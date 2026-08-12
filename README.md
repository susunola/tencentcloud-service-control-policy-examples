<p align="center">
  <b>English</b> &nbsp;|&nbsp;
  <a href="README.zh-CN.md">简体中文</a>
</p>

# Tencent Cloud Service Control Policy Examples

## Scope and safety

These examples target **Tencent Cloud Organization (TCO) service control policies**, not AWS Organizations SCPs. They are reference templates, not a claim that every action has been tested in every Tencent Cloud account or region.

Always test in a dedicated organization node before binding a policy to production. A deny policy can block console workflows, automation, service-linked operations, and incident response.

TCO SCPs define an organization-level permission boundary; they do not replace CAM identity policies or resource policies. Tencent Cloud evaluates SCPs through the organization hierarchy before CAM. At every hierarchy level, an applicable allow is required to continue evaluation. Keep the system `FullQcloudAccess` policy bound where broad access is intended, then add deny guardrails. If you replace it with a custom allow policy, that policy becomes an allow boundary and must include every operation needed at that level.

Service-linked roles are not controlled by TCO SCPs. Root-account controls and MFA enforcement are not represented here because Tencent Cloud does not expose the AWS-style root/MFA condition keys used for those controls in TCO SCPs.

## Policy syntax supported here

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "deny",
      "action": ["service:ActionName"],
      "resource": ["qcs::service:region:account:resource"],
      "condition": {
        "string_equal": {
          "qcs:resource_tag": "key&value"
        }
      }
    }
  ]
}
```

| Field | Description |
|---|---|
| `version` | Always `"2.0"`. |
| `effect` | `deny` for a guardrail; `allow` is used only for the tag-constrained allow-boundary example. |
| `action` | Tencent Cloud CAM action names such as `cvm:TerminateInstances`. `not_action` is not used or supported by this repository. |
| `resource` | `*` or a six-segment QCS resource. `not_resource` is not used or supported by this repository. |
| `condition` | Optional. Use only documented general or service-level condition keys for the selected action. |

The documented general condition keys are `qcs:current_time`, `qcs:ip`, `qcs:resource_tag`, and `qcs:request_tag`. Service-level examples in this repository use `cvm:region`, `cvm:instance_type`, `vpc:region`, and `cos:x-cos-acl`. Condition-key names are case-sensitive.

## Categories

| Category | Count | Purpose |
|---|---:|---|
| [Privileged Access Controls](Privileged-access-controls/README.md) | 5 | Protect organization membership, CAM users, roles, billing, and federation. |
| [Region Controls](Region-controls/README.md) | 1 | Restrict CVM and VPC operations to approved regions. |
| [Deny Changes to Security Services](Deny-changes-to-security-services/README.md) | 6 | Protect CloudAudit, WAF, CWP, CSIP, and Monitor controls. |
| [Protect Cloud Platform Resource](Protect-cloud-platform-resource/README.md) | 4 | Protect VPC, KMS, SCF, and CLB resources. |
| [Sensitive Data Protection](Sensitive-data-protection/README.md) | 2 | Protect COS data and public ACLs. |
| [Service-Specific Controls](Service-specific-controls/README.md) | 11 | COS, CVM, CAM, and VPC controls. |
| [Services in Scope Compliance](Services-in-scope-compliance/README.md) | 1 | A tag-constrained allow boundary for selected create operations. |

## Start with these policies

| Policy | Goal |
|---|---|
| [Deny member leave operations](Privileged-access-controls/deny-member-leave-organization.json) | Prevent member accounts from leaving or being removed from the organization through the covered APIs. |
| [Restrict CVM and VPC regions](Region-controls/deny-unapproved-cvm-and-vpc-regions.json) | Deny CVM/VPC requests whose service-level region is not approved. |
| [Protect security services](Deny-changes-to-security-services/README.md) | Prevent changes to audit, monitoring, and security controls. |
| [Protect sensitive COS buckets](Service-specific-controls/COS/deny-deleting-cos-buckets-or-objects.json) | Block deletion of a named bucket and its objects. |
| [Require tags with an allow boundary](Services-in-scope-compliance/allow-actions-with-required-tags.json) | Allow selected create operations only when the request includes the required tag value. Replace, do not stack with, an unrestricted allow policy at the target node. |

## Validation

```bash
python3 tests/test_policies.py
```

The validator checks JSON encoding, structure, Tencent Cloud-only elements, documented condition keys and operators, QCS shape, policy size, placeholders, duplicate actions, README references, and repository completeness. It intentionally fails on AWS-style `not_action`, `not_resource`, principal-tag, root-user, MFA, and ARN constructs.

## Known capability boundaries

See [UNSUPPORTED.md](UNSUPPORTED.md) for controls removed because Tencent Cloud TCO cannot express them safely with the documented SCP/CAM model. For controls that need principal identity, MFA, public-IP request parameters, or external-sharing targets, use the relevant CAM policy, resource policy, product control, or an out-of-band governance workflow instead of a fake SCP condition.

## Documentation

| Resource | Link |
|---|---|
| TCO service control policy overview | https://www.tencentcloud.com/document/product/1031/51871 |
| Enable service control policies | https://cloud.tencent.com/document/product/850/83576 |
| CAM policy syntax | https://cloud.tencent.com/document/product/598/10604 |
| CAM condition keys and operators | https://cloud.tencent.com/document/product/598/10608 |
| CVM condition keys | https://cloud.tencent.com/document/product/454/10313 |
| COS condition keys | https://cloud.tencent.com/document/product/239/71306 |
| Tag-constrained policy example | https://cloud.tencent.com/document/api/1081/104657 |

## Contributing

Run `python3 tests/test_policies.py` before opening a pull request. When adding a policy, cite the Tencent Cloud API or CAM documentation for every condition key and explain the blast radius, required placeholders, test scope, and rollback path.

## License

MIT-0 License — see [LICENSE](LICENSE).
