<p align="center">
  <b>English</b> &nbsp;|&nbsp;
  <a href="README.zh-CN.md">简体中文</a>
</p>

# Tencent Cloud Service Control Policy Examples

## Overview

**The SCP examples in this repository are for reference only.** Do not attach SCPs without thoroughly testing the impact on accounts. Test in a separate organization or OU before deploying to broader scopes.

[Service Control Policies (SCPs)](https://www.tencentcloud.com/document/product/1031/51871) are coarse-grained guardrails in Tencent Cloud Organization (TCO). They do not grant permissions — administrators must still attach [identity-based](https://www.tencentcloud.com/document/product/598/10601) or [resource-based](https://www.tencentcloud.com/document/product/598/10602) policies. Effective permissions are the **logical intersection** of the SCP and the identity/resource policy.

Organize accounts by **function, compliance requirement, or common controls** — not by org-chart hierarchy. For a deep-dive on SCP evaluation, see [SCP Evaluation Logic](https://www.tencentcloud.com/document/product/1031/51871).

### Policy Syntax

Uses standard Tencent Cloud CAM policy syntax:

```json
{
    "version": "2.0",
    "statement": [
        {
            "effect": "deny",
            "action": ["service:ActionName"],
            "resource": ["qcs::service:region:account:resource"],
            "condition": { }
        }
    ]
}
```

| Field | Description |
|-------|-------------|
| `version` | Always `"2.0"` |
| `effect` | `"deny"` (explicit deny) or `"allow"` |
| `action` | `service:ActionName`, e.g. `cvm:TerminateInstances`. Supports `*` and `not_action` |
| `resource` | Six-segment QCS format `qcs::service:region:account:resource`, or `*`. Supports `not_resource` |
| `condition` | Optional. Supports string/numeric/date/IP/boolean/null operators |

> **Note**: Examples use a **deny-list strategy** — attach an allow policy (e.g. `FullQcloudAccess`) alongside, and grant permissions via identity/resource policies.

### Categories

| Category | Count | Purpose |
|----------|-------|---------|
| [Privileged Access Controls](Privileged-access-controls/README.md) | 7 | Least-privilege enforcement for roles and apps |
| [Region Controls](Region-controls/README.md) | 1 | Block unapproved regions |
| [Deny Changes to Security Services](Deny-changes-to-security-services/README.md) | 6 | Protect CloudAudit, WAF, CWP, CSIP, Monitor |
| [Protect Cloud Platform Resource](Protect-cloud-platform-resource/README.md) | 5 | Guard VPC/KMS/SCF/CBS/CLB from deletion |
| [Sensitive Data Protection](Sensitive-data-protection/README.md) | 4 | Prevent public COS, open SGs, data exfiltration |
| [Service-Specific Controls](Service-specific-controls/README.md) | 11 | COS/CVM/CAM/VPC service-level policies |
| [Services in Scope Compliance](Services-in-scope-compliance/README.md) | 2 | MFA enforcement, tagging compliance |

### Top SCPs to Start With

| # | Policy | Goal |
|---|--------|------|
| 1 | [Deny member accounts from leaving the organization](Privileged-access-controls/deny-member-leave-organization.json) | Prevent account detachment from TCO |
| 2 | [Only allow approved regions](Region-controls/deny-access-based-on-requested-region.json) | Region allowlist |
| 3 | [Prevent root credentials management](Privileged-access-controls/prevent-root-credentials-management.json) | Centralize root key and login control |
| 4 | [Deny root user actions except exceptions](Privileged-access-controls/deny-root-user-actions-except-exceptions.json) | Restrict root to specific operations |
| 5 | [Deny changes to security services](Deny-changes-to-security-services/README.md) | Guardrails for CloudAudit, WAF, CWP |
| 6 | [Protect sensitive COS buckets](Service-specific-controls/COS/deny-deleting-cos-buckets-or-objects.json) | Block accidental/malicious deletion |

### Testing

```bash
cd tests
python3 test_policies.py
```

831 assertions across 5 levels: syntax (encoding/BOM/whitespace), structural (required keys, mutual exclusion), semantic (service prefixes, condition operators, QCS format, no AWS refs), consistency (README cross-reference, file completeness), and best practices (placeholder format, not_action safety, indentation).

## Documentation

| Resource | Link |
|----------|------|
| SCP Overview | https://www.tencentcloud.com/document/product/1031/51871 |
| CAM Policy Syntax | https://www.tencentcloud.com/document/product/598/10603 |
| TCO Management | https://www.tencentcloud.com/document/product/1031 |
| CAM Best Practices | https://www.tencentcloud.com/document/product/598/10592 |

## Contributing

Bug reports and pull requests welcome. Run the test suite before submitting.

## License

MIT-0 License — see [LICENSE](LICENSE).
