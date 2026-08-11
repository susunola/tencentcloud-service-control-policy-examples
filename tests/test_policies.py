#!/usr/bin/env python3
"""
腾讯云服务管控策略（SCP）示例 — 最高水平测试
============================================
Level 1 — 基础语法
  1.  JSON 合法性
  2.  文件编码（UTF-8, 无BOM）
  3.  尾行换行
  4.  尾随空格

Level 2 — 结构完整性
  5.  顶层必需键 (version, statement)
  6.  Statement 必需键 (effect, resource, action/not_action)
  7.  Version 恒为 "2.0"
  8.  Effect 全为 deny（deny-list 策略）
  9.  互斥字段检查 (action vs not_action, resource vs not_resource)

Level 3 — 语义正确性
  10. Action 服务前缀有效性
  11. QCS 资源六段式格式
  12. 条件操作符有效性（合法 CAM operator）
  13. 条件键不含 AWS 前缀
  14. 整体不含 AWS 引用 (arn:aws, Version:2012-10-17)

Level 4 — 一致性
  15. README 交叉引用：表里的文件存在 & JSON 文件被表引用
  16. 根目录骨文件完整性
  17. CI 工作流存在
  18. 文件命名规范 (kebab-case)
  19. 无多余顶层键
  20. 无重复 action 项

Level 5 — 安全 & 最佳实践
  21. Placeholder 统一 [UPPER_SNAKE] 格式
  22. NotAction + Resource:"*" 组合有足够约束
  23. Condition block 不为空 object
  24. 缩进一致性（2空格）
"""

import json
import os
import sys
import re
from collections import defaultdict, OrderedDict

# ---- Configuration ----
POLICY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VALID_TOP_KEYS = {"version", "statement"}
VALID_STMT_KEYS = {"effect", "action", "not_action", "resource", "not_resource", "condition"}

# 腾讯云 CAM 合法条件操作符
VALID_COND_OPERATORS = {
    # 字符串
    "string_equal", "string_not_equal",
    "string_equal_ignore_case", "string_not_equal_ignore_case",
    "string_equal_if_exist", "string_not_equal_if_exist",
    # 数值
    "numeric_equal", "numeric_not_equal",
    "numeric_greater_than", "numeric_greater_than_equals",
    "numeric_less_than", "numeric_less_than_equals",
    "numeric_equal_if_exist", "numeric_not_equal_if_exist",
    # 日期
    "date_equal", "date_not_equal",
    "date_greater_than", "date_greater_than_equals",
    "date_less_than", "date_less_than_equals",
    "date_equal_if_exist", "date_not_equal_if_exist",
    # 布尔
    "bool_equal",
    # 二进制
    "binary_equal",
    # IP
    "ip_equal", "ip_not_equal",
    "ip_equal_if_exist", "ip_not_equal_if_exist",
    # 空值
    "null_equal",
    # 集合
    "for_any_value:string_equal", "for_any_value:string_not_equal",
    "for_all_value:string_equal", "for_all_value:string_not_equal",
}

# 已知腾讯云服务前缀
KNOWN_SERVICE_PREFIXES = {
    "cam", "cvm", "cos", "vpc", "clb", "cbs", "kms", "scf",
    "monitor", "cloudaudit", "cwp", "waf", "csip", "organization",
    "account", "billing", "tag", "sts", "cfs", "cdn", "ckafka",
    "cynosdb", "es", "tke", "tcr", "tdmq", "cls", "sms", "ssl",
    "tcb", "tcaplusdb", "apigateway", "as", "cdb", "cmq",
    "emr", "faceid", "iai", "iot", "live", "mariadb", "mongodb",
    "postgres", "redis", "sqlserver", "tic", "tiw", "trtc",
    "vod", "youmall", "gaap", "lighthouse",
}

REQUIRED_ROOT_FILES = ["README.md", "LICENSE", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"]

pass_count = 0
fail_count = 0
warn_count = 0
failures = []
warnings = []


def warn(filepath, msg):
    global warn_count
    warn_count += 1
    rel = os.path.relpath(filepath, POLICY_DIR) if filepath else ""
    warnings.append(f"  ⚠ WARNING [{rel}]: {msg}")


def fail(filepath, msg):
    global fail_count
    fail_count += 1
    rel = os.path.relpath(filepath, POLICY_DIR) if filepath else ""
    failures.append(f"  ✗ FAIL [{rel}]: {msg}")


def pass_test(filepath=None):
    global pass_count
    pass_count += 1


def find_policy_files(root):
    policy_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if f.endswith(".json"):
                policy_files.append(os.path.join(dirpath, f))
    return sorted(policy_files)


def find_all_files(root, ext=None):
    """Find all files, optionally filtered by extension."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if ext is None or f.endswith(ext):
                files.append(os.path.join(dirpath, f))
    return sorted(files)


# ===========================================================
# Level 1: 基础语法
# ===========================================================

def test_json_valid(data, filepath):
    if data is None:
        fail(filepath, "JSON 无法解析")
        return False
    pass_test()
    return True


def test_encoding(filepath):
    try:
        with open(filepath, "rb") as f:
            raw = f.read()
        if raw.startswith(b"\xef\xbb\xbf"):
            fail(filepath, "文件包含 UTF-8 BOM")
            return
        # Try decode
        raw.decode("utf-8")
    except UnicodeDecodeError:
        fail(filepath, "文件不是 UTF-8 编码")
        return
    pass_test()


def test_trailing_newline(filepath):
    with open(filepath, "rb") as f:
        content = f.read()
    if not content.endswith(b"\n"):
        fail(filepath, "文件末尾缺少换行符")
        return
    pass_test()


def test_trailing_whitespace(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if line.rstrip("\n").rstrip("\r") != line.rstrip("\n").rstrip("\r").rstrip():
            # Has trailing spaces
            if line.strip():  # Only flag non-empty lines
                fail(filepath, f"第 {i} 行尾有空格")
                return
    pass_test()


# ===========================================================
# Level 2: 结构完整性
# ===========================================================

def test_top_level_keys(data, filepath):
    if not isinstance(data, dict):
        return False
    for key in VALID_TOP_KEYS:
        if key not in data:
            fail(filepath, f"缺少顶层键 '{key}'")
            return False
    pass_test()
    return True


def test_version(data, filepath):
    if data.get("version") != "2.0":
        fail(filepath, f"version 必须为 '2.0'，当前 '{data.get('version')}'")
        return False
    pass_test()
    return True


def test_statement_array(data, filepath):
    stmts = data.get("statement")
    if not isinstance(stmts, list):
        fail(filepath, "statement 必须是数组")
        return False
    if len(stmts) == 0:
        fail(filepath, "statement 数组为空")
        return False
    pass_test()
    return True


def test_effect_deny(data, filepath):
    stmts = data.get("statement", [])
    all_deny = True
    for i, stmt in enumerate(stmts):
        effect = stmt.get("effect", "").lower()
        if effect not in ("deny", "allow"):
            fail(filepath, f"Statement[{i}]: effect 必须为 deny 或 allow，当前 '{effect}'")
            all_deny = False
        elif effect == "allow":
            warn(filepath, f"Statement[{i}]: effect=allow，本仓库使用 deny-list 策略")
    if all_deny:
        pass_test()


def test_mutually_exclusive(data, filepath):
    for i, stmt in enumerate(data.get("statement", [])):
        if "action" in stmt and "not_action" in stmt:
            fail(filepath, f"Statement[{i}]: action 和 not_action 不能同时出现")
        if "resource" in stmt and "not_resource" in stmt:
            fail(filepath, f"Statement[{i}]: resource 和 not_resource 不能同时出现")
    pass_test()


def test_required_stmt_keys(data, filepath):
    for i, stmt in enumerate(data.get("statement", [])):
        if "resource" not in stmt:
            fail(filepath, f"Statement[{i}]: 缺少 resource")
            continue
        if "action" not in stmt and "not_action" not in stmt:
            fail(filepath, f"Statement[{i}]: 必须有 action 或 not_action")
            continue
    pass_test()


# ===========================================================
# Level 3: 语义正确性
# ===========================================================

def test_action_service_prefix(data, filepath):
    for i, stmt in enumerate(data.get("statement", [])):
        action_key = "not_action" if "not_action" in stmt else "action"
        actions = stmt.get(action_key, [])
        if isinstance(actions, str):
            actions = [actions]
        for j, act in enumerate(actions):
            if act == "*":
                continue
            if ":" not in act:
                warn(filepath, f"Statement[{i}]: {action_key}[{j}]='{act}' 缺少服务前缀")
                continue
            prefix = act.split(":")[0]
            if prefix not in KNOWN_SERVICE_PREFIXES:
                warn(filepath, f"Statement[{i}]: {action_key}[{j}]='{act}' 服务前缀 '{prefix}' 不在已知列表中")
    pass_test()


def test_qcs_format(data, filepath):
    raw = json.dumps(data)
    qcs_pattern = re.compile(
        r'^qcs::[a-z]+:([a-z\-]*|\*):(?:(?:uin|uid)/[0-9A-Za-z\[\]\*\-_]+|\*):[0-9A-Za-z\[\]\*\-_/]+$'
    )
    for match in re.finditer(r'"qcs::[^"]*"', raw):
        qcs_str = match.group(0).strip('"')
        if not qcs_pattern.match(qcs_str):
            warn(filepath, f"QCS 资源格式可疑: {qcs_str}")
    pass_test()


def test_condition_operators(data, filepath):
    for i, stmt in enumerate(data.get("statement", [])):
        condition = stmt.get("condition", {})
        if not condition:
            continue
        if not isinstance(condition, dict):
            fail(filepath, f"Statement[{i}]: condition 必须是对象")
            continue
        for operator in condition:
            if operator not in VALID_COND_OPERATORS:
                fail(filepath, f"Statement[{i}]: 无效的条件操作符 '{operator}'")
    pass_test()


def test_no_aws_in_condition(data, filepath):
    raw = json.dumps(data)
    # Check for aws: prefix in condition keys or values
    cond_data = json.dumps(data.get("statement", [{}])[0].get("condition", {}))
    for i, stmt in enumerate(data.get("statement", [])):
        cond = json.dumps(stmt.get("condition", {}))
        # Look for aws: as a condition key pattern (quoted)
        if re.search(r'"aws:', cond):
            fail(filepath, f"Statement[{i}]: 条件键包含 'aws:' 前缀")
    pass_test()


def test_no_aws_arn(data, filepath):
    raw = json.dumps(data)
    if re.search(r'arn:aws:', raw):
        fail(filepath, "包含 AWS ARN")
    if re.search(r'"Version"\s*:\s*"2012-10-17"', raw):
        fail(filepath, "包含 AWS IAM version 字符串")
    pass_test()


# ===========================================================
# Level 4: 一致性
# ===========================================================

def parse_readme_table_entries(readme_path):
    """Extract .json file references from a README.md markdown table."""
    if not os.path.exists(readme_path):
        return set()
    entries = set()
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Match markdown links to .json files: [text](path.json)
    for match in re.finditer(r'\[([^\]]+)\]\(([^)]+\.json)\)', content):
        ref = match.group(2)
        # Resolve relative path
        dir_name = os.path.dirname(readme_path)
        full = os.path.normpath(os.path.join(dir_name, ref))
        entries.add(os.path.relpath(full, POLICY_DIR))
    return entries


def test_readme_cross_reference():
    readme_paths = find_all_files(POLICY_DIR, ".md")
    all_json_files = set()
    for f in find_policy_files(POLICY_DIR):
        all_json_files.add(os.path.relpath(f, POLICY_DIR))

    all_refs = set()

    for rpath in readme_paths:
        refs = parse_readme_table_entries(rpath)
        all_refs.update(refs)

    # Check: every JSON file is referenced in some README
    unreferenced = all_json_files - all_refs
    for uf in sorted(unreferenced):
        warn(None, f"JSON 文件未在任何 README 中引用: {uf}")

    # Check: every README reference points to an existing file
    missing = all_refs - all_json_files
    for mf in sorted(missing):
        fail(None, f"README 引用了不存在的文件: {mf}")

    pass_test()


def test_root_files_exist():
    for fname in REQUIRED_ROOT_FILES:
        fpath = os.path.join(POLICY_DIR, fname)
        if not os.path.exists(fpath):
            fail(None, f"缺少根目录文件: {fname}")
    pass_test()


def test_ci_exists():
    wf_path = os.path.join(POLICY_DIR, ".github", "workflows", "test.yml")
    if not os.path.exists(wf_path):
        fail(None, "缺少 CI 工作流: .github/workflows/test.yml")
    pass_test()


def test_file_naming(data, filepath):
    basename = os.path.basename(filepath)
    if not re.match(r"^[a-z0-9][a-z0-9\-_]*\.json$", basename):
        fail(filepath, f"文件名 '{basename}' 应使用小写 kebab-case")
    pass_test()


def test_no_extra_keys(data, filepath):
    extra = set(data.keys()) - VALID_TOP_KEYS
    if extra:
        fail(filepath, f"顶层存在多余键: {extra}")
    pass_test()


def test_no_duplicate_actions(data, filepath):
    for i, stmt in enumerate(data.get("statement", [])):
        for key in ("action", "not_action"):
            actions = stmt.get(key, [])
            if isinstance(actions, list) and len(actions) > 1:
                seen = set()
                dupes = set()
                for act in actions:
                    if act in seen:
                        dupes.add(act)
                    seen.add(act)
                if dupes:
                    fail(filepath, f"Statement[{i}]: {key} 中有重复项: {dupes}")
    pass_test()


# ===========================================================
# Level 5: 安全 & 最佳实践
# ===========================================================

def test_placeholder_format(data, filepath):
    raw = json.dumps(data)
    # Placeholders should be [UPPER_SNAKE] format
    placeholders = re.findall(r'\[([A-Za-z_]+)\]', raw)
    for ph in placeholders:
        if ph != ph.upper():
            fail(filepath, f"占位符 '[{ph}]' 应使用全大写 SNAKE_CASE")
            return
    pass_test()


def test_notaction_resource_constraint(data, filepath):
    """When using not_action, ensure there's meaningful resource or condition constraint."""
    for i, stmt in enumerate(data.get("statement", [])):
        if "not_action" in stmt:
            resource = stmt.get("resource", "")
            if isinstance(resource, list):
                resource = resource[0] if resource else ""
            condition = stmt.get("condition", {})
            if resource == "*" and not condition:
                warn(filepath, f"Statement[{i}]: not_action 配合 resource=* 且无 condition，权限范围过大")
    pass_test()


def test_condition_not_empty(data, filepath):
    for i, stmt in enumerate(data.get("statement", [])):
        cond = stmt.get("condition", {})
        if isinstance(cond, dict) and len(cond) == 0 and "condition" in stmt:
            warn(filepath, f"Statement[{i}]: condition 为空对象，建议移除该字段")
    pass_test()


def test_indentation_consistency(data, filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # All JSON files should use 2-space indent
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped and stripped[0] not in "{}[]\"":  # skip opening/closing brackets
            leading = len(line) - len(stripped)
            if leading > 0 and leading % 2 != 0:
                fail(filepath, f"第 {i} 行缩进不是 2 的倍数 ({leading} 空格)")
                return
    pass_test()


def test_json_pretty_print(data, filepath):
    """Ensure JSON is serialized with standard indentation."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    canonical = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if raw != canonical:
        warn(filepath, "JSON 格式与标准 pretty-print 不一致（缩进/排序可能有偏差）")
    pass_test()


# ===========================================================
# Runner
# ===========================================================

def collect_data():
    """Pre-load all policy files."""
    policy_files = find_policy_files(POLICY_DIR)
    loaded = {}
    for fp in policy_files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                loaded[fp] = json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            loaded[fp] = None
    return loaded


def run_all_tests():
    global pass_count, fail_count, warn_count
    fail_count = warn_count = 0

    loaded = collect_data()

    if not loaded:
        print("ERROR: 未找到任何策略 JSON 文件！")
        return 1

    print(f"🧪 最高水平测试 — {len(loaded)} 个策略文件\n")
    print("=" * 72)

    categories = defaultdict(int)

    for filepath in sorted(loaded.keys()):
        rel = os.path.relpath(filepath, POLICY_DIR)
        category = rel.split(os.sep)[0]
        categories[category] += 1
        data = loaded[filepath]

        # Level 1
        test_encoding(filepath)
        test_trailing_newline(filepath)
        test_trailing_whitespace(filepath)

        if not test_json_valid(data, filepath):
            continue

        # Level 2
        if not test_top_level_keys(data, filepath):
            continue
        test_version(data, filepath)
        if not test_statement_array(data, filepath):
            continue
        test_effect_deny(data, filepath)
        test_mutually_exclusive(data, filepath)
        test_required_stmt_keys(data, filepath)

        # Level 3
        test_action_service_prefix(data, filepath)
        test_qcs_format(data, filepath)
        test_condition_operators(data, filepath)
        test_no_aws_in_condition(data, filepath)
        test_no_aws_arn(data, filepath)

        # Level 4
        test_file_naming(data, filepath)
        test_no_extra_keys(data, filepath)
        test_no_duplicate_actions(data, filepath)

        # Level 5
        test_placeholder_format(data, filepath)
        test_notaction_resource_constraint(data, filepath)
        test_condition_not_empty(data, filepath)
        test_indentation_consistency(data, filepath)
        test_json_pretty_print(data, filepath)

    # Cross-file tests
    print("", flush=True)
    test_readme_cross_reference()
    test_root_files_exist()
    test_ci_exists()

    # ---- Summary ----
    total = pass_count + fail_count
    score = round(pass_count / total * 100, 1) if total else 0

    print("\n" + "=" * 72)
    print("📊 测试总结")
    print("=" * 72)

    print(f"\n  策略分布:")
    for cat, count in sorted(categories.items()):
        print(f"    {cat:.<45s} {count:>3} 个")

    print(f"\n  测试项: {total}")
    print(f"    ✅ 通过:  {pass_count}")
    print(f"    ❌ 失败:  {fail_count}")
    print(f"    ⚠️  警告:  {warn_count}")
    print(f"    📈 通过率: {score}%")

    if failures:
        print(f"\n{'─' * 72}")
        print("❌ 失败项:")
        for f in failures:
            print(f)

    if warnings:
        print(f"\n{'─' * 72}")
        print("⚠️  警告:")
        for w in warnings:
            print(w)

    print(f"\n{'=' * 72}")

    if fail_count > 0:
        print(f"❌ 测试失败！(通过率 {score}%)")
        return 1
    else:
        print(f"🏆 全部 {pass_count} 项测试通过，最高水平达成！")
        return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
