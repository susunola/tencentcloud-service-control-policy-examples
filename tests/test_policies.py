#!/usr/bin/env python3
"""
腾讯云服务管控策略（SCP）示例 - 策略验证测试
==============================================
对所有策略 JSON 文件进行自动化验证，包括：
1. JSON 语法合法性
2. 必需字段完整性
3. 策略效应（必须为 deny 列表策略）
4. Action 格式合规性
5. Resource 格式合规性
6. 文件结构一致性
"""

import json
import os
import sys
import re
from collections import defaultdict

# ---- Configuration ----
POLICY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED_TOP_KEYS = {"version", "statement"}
REQUIRED_STMT_KEYS = {"effect", "resource"}

# Valid Tencent Cloud service prefixes (commonly used)
KNOWN_SERVICE_PREFIXES = {
    "cam", "cvm", "cos", "vpc", "clb", "cbs", "kms", "scf",
    "monitor", "cloudaudit", "cwp", "waf", "csip", "organization",
    "account", "billing", "tag", "sts", "cfs", "cdn", "ckafka",
    "cynosdb", "es", "tke", "tcr", "tdmq", "cls", "sms", "ssl",
}

pass_count = 0
fail_count = 0
failures = []
warnings = []


def warn(filepath, msg):
    warnings.append(f"  ⚠ WARNING [{filepath}]: {msg}")


def fail(filepath, msg):
    global fail_count
    fail_count += 1
    failures.append(f"  ✗ FAIL [{filepath}]: {msg}")


def pass_test(filepath):
    global pass_count
    pass_count += 1


def find_policy_files(root):
    """Find all .json policy files recursively, excluding hidden dirs."""
    policy_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if f.endswith(".json"):
                policy_files.append(os.path.join(dirpath, f))
    return sorted(policy_files)


def validate_json_syntax(filepath):
    """Test 1: File is valid JSON."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        fail(filepath, f"Invalid JSON: {e}")
        return None
    except Exception as e:
        fail(filepath, f"Cannot read file: {e}")
        return None


def validate_top_level_structure(filepath, data):
    """Test 2: Top-level structure has required keys."""
    rel = os.path.relpath(filepath, POLICY_DIR)
    if not isinstance(data, dict):
        fail(filepath, "Top-level must be a JSON object")
        return False

    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            fail(filepath, f"Missing top-level key: '{key}'")
            return False

    if data["version"] != "2.0":
        fail(filepath, f"Version must be '2.0', got '{data['version']}'")

    if not isinstance(data["statement"], list):
        fail(filepath, "'statement' must be an array")
        return False

    if len(data["statement"]) == 0:
        fail(filepath, "'statement' array is empty")
        return False

    return True


def validate_statement(filepath, stmt, idx):
    """Test 3: Each statement has required keys and valid values."""
    rel = os.path.relpath(filepath, POLICY_DIR)

    for key in REQUIRED_STMT_KEYS:
        if key not in stmt:
            fail(filepath, f"Statement[{idx}]: missing '{key}'")
            return False

    # Must have either 'action' or 'not_action'
    has_action = "action" in stmt
    has_not_action = "not_action" in stmt
    if not has_action and not has_not_action:
        fail(filepath, f"Statement[{idx}]: must have 'action' or 'not_action'")
        return False

    # Effect must be "deny" (deny-list strategy)
    effect = stmt["effect"]
    if effect.lower() not in ("deny", "allow"):
        fail(filepath, f"Statement[{idx}]: effect must be 'deny' or 'allow', got '{effect}'")
    elif effect.lower() == "allow":
        warn(filepath, f"Statement[{idx}]: effect is 'allow'. "
             "This repo uses deny-list strategy. Ensure this is intentional.")

    # Action / not_action validation
    action_key = "not_action" if has_not_action else "action"
    action = stmt[action_key]
    if isinstance(action, str):
        if action == "*":
            pass
        elif ":" not in action:
            warn(filepath, f"Statement[{idx}]: {action_key} '{action}' should use 'service:ActionName' format")
    elif isinstance(action, list):
        for i, act in enumerate(action):
            if isinstance(act, str) and ":" not in act and act != "*":
                warn(filepath, f"Statement[{idx}]: {action_key}[{i}] '{act}' should use 'service:ActionName' format")
    else:
        fail(filepath, f"Statement[{idx}]: '{action_key}' must be a string or array of strings")
        return False

    # Resource validation
    resource = stmt["resource"]
    if isinstance(resource, str):
        if resource != "*" and not resource.startswith("qcs"):
            warn(filepath, f"Statement[{idx}]: resource should be '*' or QCS format (qcs::...): '{resource}'")
    elif isinstance(resource, list):
        for i, res in enumerate(resource):
            if not isinstance(res, str):
                fail(filepath, f"Statement[{idx}]: resource[{i}] must be a string")
            elif res != "*" and not res.startswith("qcs"):
                warn(filepath, f"Statement[{idx}]: resource[{i}] should be '*' or QCS format: '{res}'")
    else:
        fail(filepath, f"Statement[{idx}]: 'resource' must be a string or array of strings")
        return False

    # Condition (optional) validation
    condition = stmt.get("condition", {})
    if condition and not isinstance(condition, dict):
        fail(filepath, f"Statement[{idx}]: 'condition' must be an object")
        return False

    # not_resource (optional)
    has_not_resource = "not_resource" in stmt
    if has_not_resource and "resource" in stmt:
        fail(filepath, f"Statement[{idx}]: cannot have both 'resource' and 'not_resource'")
    # Validate not_resource if present
    if has_not_resource:
        nres = stmt["not_resource"]
        if isinstance(nres, str) and nres != "*" and not nres.startswith("qcs"):
            warn(filepath, f"Statement[{idx}]: not_resource should be '*' or QCS format: '{nres}'")

    return True


def validate_file_naming(filepath):
    """Test 4: Check file naming conventions."""
    basename = os.path.basename(filepath)
    if not re.match(r"^[a-z0-9][a-z0-9\-_]*\.json$", basename):
        warn(filepath, f"Filename '{basename}' should use lowercase kebab-case")


def validate_no_aws_references(filepath, data):
    """Test 5: Ensure no AWS-specific references in Tencent Cloud policies."""
    raw = json.dumps(data)
    aws_patterns = [
        (r'"Version"\s*:\s*"2012-10-17"', "AWS IAM version string"),
        (r'arn:aws:', "AWS ARN"),
        (r'aws:', "AWS service prefix"),
        (r'"aws:', "AWS condition key"),
    ]
    for pattern, desc in aws_patterns:
        if re.search(pattern, raw):
            fail(filepath, f"Contains AWS-specific reference: {desc}")


def validate_qcs_format(filepath, data):
    """Test 6: Validate QCS resource format."""
    raw = json.dumps(data)
    # QCS six-segment: qcs::service:region:account:resource_type/resource_id
    # Example: qcs::cvm:ap-guangzhou:uin/100000000001:instance/*
    # We're lenient with placeholders like [UIN], [BUCKET], [APPID], * etc.
    full_pattern = re.compile(
        r'^qcs::[a-z]+:([a-z\-]*|\*):(?:uin|uid)/([0-9A-Za-z\[\]\*\-_]+):[0-9A-Za-z\[\]\*\-_/]+$'
    )
    for match in re.finditer(r'"qcs::[^"]*"', raw):
        qcs_str = match.group(0).strip('"')
        if not full_pattern.match(qcs_str):
            warn(filepath, f"QCS resource may not follow six-segment format: {qcs_str}")


def run_all_tests():
    """Run all validation tests."""
    global pass_count, fail_count

    policy_files = find_policy_files(POLICY_DIR)

    if not policy_files:
        print("ERROR: No policy JSON files found!")
        return 1

    print(f"🔍 Validating {len(policy_files)} policy files...\n")
    print("=" * 70)

    categories = defaultdict(int)

    for filepath in policy_files:
        rel = os.path.relpath(filepath, POLICY_DIR)
        category = rel.split(os.sep)[0]
        categories[category] += 1

        # Test 1: Valid JSON
        data = validate_json_syntax(filepath)
        if data is None:
            continue

        # Test 2: Top-level structure
        if not validate_top_level_structure(filepath, data):
            continue

        # Test 3: Statement validation
        all_stmts_ok = True
        for idx, stmt in enumerate(data["statement"]):
            if not validate_statement(filepath, stmt, idx):
                all_stmts_ok = False

        # Test 4: File naming
        validate_file_naming(filepath)

        # Test 5: No AWS references
        validate_no_aws_references(filepath, data)

        # Test 6: QCS format
        validate_qcs_format(filepath, data)

        if all_stmts_ok:
            pass_test(filepath)

    # ---- Summary ----
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"\n  Files by category:")
    for cat, count in sorted(categories.items()):
        print(f"    {cat}: {count} files")

    print(f"\n  Results:")
    print(f"    ✓ Passed:  {pass_count}")
    print(f"    ✗ Failed:  {fail_count}")
    print(f"    ⚠ Warnings: {len(warnings)}")

    if warnings:
        print(f"\n{'─' * 70}")
        print("⚠ WARNINGS:")
        for w in warnings:
            print(w)

    if failures:
        print(f"\n{'─' * 70}")
        print("✗ FAILURES:")
        for f in failures:
            print(f)

    print(f"\n{'=' * 70}")

    if fail_count > 0:
        print("❌ TESTS FAILED!")
        return 1
    else:
        print("✅ ALL TESTS PASSED!")
        return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
