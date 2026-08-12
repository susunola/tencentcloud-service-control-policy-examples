#!/usr/bin/env python3
"""Validate Tencent Cloud TCO service control policy examples.

The checks are deliberately Tencent Cloud-specific. Passing JSON syntax is not
sufficient: a policy with an AWS condition key can parse successfully and still
provide no protection in Tencent Cloud.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

POLICY_DIR = Path(__file__).resolve().parent.parent

VALID_TOP_KEYS = {"version", "statement"}
VALID_STATEMENT_KEYS = {"effect", "action", "resource", "condition"}
GENERAL_CONDITION_KEYS = {
    "qcs:current_time",
    "qcs:ip",
    "qcs:resource_tag",
    "qcs:request_tag",
}
SERVICE_CONDITION_OPERATORS = {
    "cos:x-cos-acl": {"string_equal", "string_not_equal"},
    "cvm:instance_type": {"string_equal", "string_not_equal"},
    "cvm:region": {"string_equal", "string_not_equal"},
    "vpc:region": {"string_equal", "string_not_equal"},
}
VALID_CONDITION_OPERATORS = {
    "string_equal",
    "string_not_equal",
    "string_equal_ignore_case",
    "string_not_equal_ignore_case",
    "string_like",
    "string_not_like",
    "numeric_equal",
    "numeric_not_equal",
    "numeric_greater_than",
    "numeric_greater_than_equal",
    "numeric_less_than",
    "numeric_less_than_equal",
    "date_equal",
    "date_not_equal",
    "date_greater_than",
    "date_greater_than_equal",
    "date_less_than",
    "date_less_than_equal",
    "bool_equal",
    "binary_equal",
    "ip_equal",
    "ip_not_equal",
    "null_equal",
    "for_any_value:string_equal",
    "for_any_value:string_not_equal",
    "for_all_value:string_equal",
    "for_all_value:string_not_equal",
}
KNOWN_SERVICE_PREFIXES = {
    "account",
    "as",
    "billing",
    "cam",
    "cbs",
    "cdn",
    "clb",
    "cloudaudit",
    "cmq",
    "cos",
    "cvm",
    "cwp",
    "csip",
    "cynosdb",
    "emr",
    "kms",
    "lighthouse",
    "monitor",
    "organization",
    "scf",
    "sts",
    "tag",
    "tcb",
    "tcr",
    "tke",
    "tdmq",
    "vpc",
    "waf",
}
REQUIRED_ROOT_FILES = {
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "UNSUPPORTED.md",
}
LEGACY_TOKENS = {
    "not_action",
    "not_resource",
    "qcs:PrincipalTag",
    "qcs:user_type",
    "qcs:MFAPresent",
    "qcs:PrincipalArn",
    "qcs:RequestTag/",
    "cbs:Encrypt",
    "vpc:CidrIp",
    "organization:TargetUin",
    "cam:RequestedAction",
}

failures: list[str] = []
warnings: list[str] = []
passes = 0


def passed() -> None:
    global passes
    passes += 1


def fail(path: Path | None, message: str) -> None:
    location = str(path.relative_to(POLICY_DIR)) if path else "repository"
    failures.append(f"[{location}] {message}")


def warn(path: Path | None, message: str) -> None:
    location = str(path.relative_to(POLICY_DIR)) if path else "repository"
    warnings.append(f"[{location}] {message}")


def policy_files() -> list[Path]:
    return sorted(POLICY_DIR.rglob("*.json"))


def read_json(path: Path) -> tuple[Any | None, str]:
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw), raw
    except json.JSONDecodeError as exc:
        fail(path, f"invalid JSON: {exc}")
        return None, raw


def test_file_encoding_and_format(path: Path, raw: str) -> None:
    encoded = path.read_bytes()
    if encoded.startswith(b"\xef\xbb\xbf"):
        fail(path, "UTF-8 BOM is not allowed")
    if not encoded.endswith(b"\n"):
        fail(path, "file must end with a newline")
    for line_number, line in enumerate(raw.splitlines(), 1):
        if line.rstrip() != line:
            fail(path, f"trailing whitespace on line {line_number}")
    passed()


def test_top_level(data: Any, path: Path) -> bool:
    if not isinstance(data, dict):
        fail(path, "top level must be an object")
        return False
    if set(data) != VALID_TOP_KEYS:
        fail(path, f"top-level keys must be exactly {sorted(VALID_TOP_KEYS)}")
    if data.get("version") != "2.0":
        fail(path, "version must be '2.0'")
    statements = data.get("statement")
    if not isinstance(statements, list) or not statements:
        fail(path, "statement must be a non-empty array")
        return False
    passed()
    return True


def test_statement_shape(data: dict[str, Any], path: Path) -> None:
    for index, statement in enumerate(data["statement"]):
        if not isinstance(statement, dict):
            fail(path, f"statement[{index}] must be an object")
            continue
        extra = set(statement) - VALID_STATEMENT_KEYS
        if extra:
            fail(path, f"statement[{index}] has unsupported keys: {sorted(extra)}")
        if statement.get("effect") not in {"allow", "deny"}:
            fail(path, f"statement[{index}] effect must be allow or deny")
        for key in ("action", "resource"):
            value = statement.get(key)
            if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
                fail(path, f"statement[{index}] {key} must be a non-empty string array")
        if "condition" in statement and not isinstance(statement["condition"], dict):
            fail(path, f"statement[{index}] condition must be an object")
    passed()


def test_actions(data: dict[str, Any], path: Path) -> None:
    for index, statement in enumerate(data["statement"]):
        actions = statement.get("action", [])
        if len(actions) != len(set(actions)):
            fail(path, f"statement[{index}] contains duplicate actions")
        for action in actions:
            if action == "*":
                continue
            if ":" not in action:
                fail(path, f"action lacks service prefix: {action}")
                continue
            prefix = action.split(":", 1)[0]
            if prefix not in KNOWN_SERVICE_PREFIXES:
                warn(path, f"service prefix is not in the local reference set: {prefix}")
    passed()


def test_conditions(data: dict[str, Any], path: Path) -> None:
    for index, statement in enumerate(data["statement"]):
        condition = statement.get("condition", {})
        for operator, key_map in condition.items():
            if operator not in VALID_CONDITION_OPERATORS:
                fail(path, f"statement[{index}] has unsupported condition operator: {operator}")
            if not isinstance(key_map, dict) or not key_map:
                fail(path, f"statement[{index}] condition operator must map to a non-empty object")
                continue
            for key, value in key_map.items():
                valid_key = key in GENERAL_CONDITION_KEYS or key in SERVICE_CONDITION_OPERATORS
                if not valid_key:
                    fail(path, f"statement[{index}] has undocumented condition key: {key}")
                if key in SERVICE_CONDITION_OPERATORS and operator not in SERVICE_CONDITION_OPERATORS[key]:
                    fail(path, f"operator {operator} is not documented for {key}")
                if not isinstance(value, (str, int, float, bool, list)):
                    fail(path, f"condition value for {key} has unsupported type")
    passed()


def test_qcs_resources(data: dict[str, Any], path: Path) -> None:
    for statement in data["statement"]:
        for resource in statement.get("resource", []):
            if resource == "*" or not resource.startswith("qcs:"):
                continue
            parts = resource.split(":")
            if len(parts) != 6 or parts[0] != "qcs" or parts[1] != "":
                fail(path, f"invalid six-segment QCS resource: {resource}")
                continue
            if not parts[2] or not parts[5]:
                fail(path, f"QCS resource has an empty service or resource segment: {resource}")
            account = parts[4]
            if account not in {"", "*"} and not re.fullmatch(r"(?:uin|uid)/[A-Za-z0-9_*\[\]-]+", account):
                fail(path, f"invalid QCS account segment: {resource}")
    passed()


def test_placeholders_and_size(data: dict[str, Any], path: Path, raw: str) -> None:
    placeholder_pattern = re.compile(r'"[^"\n]*\[([^\[\]]+)\][^"\n]*"')
    for match in placeholder_pattern.finditer(raw):
        placeholder = match.group(1)
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", placeholder):
            fail(path, f"placeholder must use UPPER_SNAKE_CASE: [{placeholder}]")
    compact_size = len(re.sub(r"\s+", "", raw))
    if compact_size > 6144:
        fail(path, f"policy exceeds the 6144-character Tencent Cloud limit: {compact_size}")
    canonical = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if raw != canonical:
        fail(path, "JSON must use canonical two-space formatting")
    passed()


def test_no_legacy_tokens(path: Path, raw: str) -> None:
    for token in LEGACY_TOKENS:
        if token in raw:
            fail(path, f"legacy or unsupported Tencent Cloud token remains: {token}")
    if "arn:aws:" in raw or '"Version":"2012-10-17"' in raw:
        fail(path, "AWS policy syntax remains")
    passed()


def readme_json_references() -> set[str]:
    references: set[str] = set()
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+\.json)\)")
    for readme in POLICY_DIR.rglob("*.md"):
        content = readme.read_text(encoding="utf-8")
        for reference in pattern.findall(content):
            target = (readme.parent / reference).resolve()
            references.add(str(target.relative_to(POLICY_DIR)))
    return references


def test_repository_consistency() -> None:
    actual = {str(path.relative_to(POLICY_DIR)) for path in policy_files()}
    referenced = readme_json_references()
    for path in sorted(actual - referenced):
        warn(None, f"policy is not linked from a README: {path}")
    for path in sorted(referenced - actual):
        fail(None, f"README links to a missing policy: {path}")
    for required in REQUIRED_ROOT_FILES:
        if not (POLICY_DIR / required).exists():
            fail(None, f"missing root file: {required}")
    workflow = POLICY_DIR / ".github" / "workflows" / "test.yml"
    if not workflow.exists():
        fail(None, "missing CI workflow")
    for readme in POLICY_DIR.rglob("*.md"):
        if "deny-access-based-on-requested-region.json" in readme.read_text(encoding="utf-8"):
            fail(readme, "legacy region policy reference remains")
    passed()


def main() -> int:
    files = policy_files()
    if not files:
        print("No policy files found")
        return 1
    for path in files:
        data, raw = read_json(path)
        test_file_encoding_and_format(path, raw)
        if data is None or not test_top_level(data, path):
            continue
        test_statement_shape(data, path)
        test_actions(data, path)
        test_conditions(data, path)
        test_qcs_resources(data, path)
        test_placeholders_and_size(data, path, raw)
        test_no_legacy_tokens(path, raw)
    test_repository_consistency()

    total = passes + len(failures)
    print(f"Validated {len(files)} policy files")
    print(f"Checks passed: {passes}")
    print(f"Failures: {len(failures)}")
    print(f"Warnings: {len(warnings)}")
    if failures:
        print("\nFailures:")
        for item in failures:
            print(f"- {item}")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
