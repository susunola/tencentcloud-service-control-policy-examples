# Tencent Cloud controls not represented as SCP examples

The following files were removed because their original behavior depended on AWS condition keys or AWS-only SCP elements. Keeping them would create a policy that looks protective but does not enforce the stated control in Tencent Cloud.

| Removed control | Why it is not kept as a TCO SCP | Better Tencent Cloud control |
|---|---|---|
| Root-user actions and root-credential management | TCO SCP does not expose the original `qcs:user_type`, `cam:RequestedAction`, or equivalent AWS root condition keys. | Manage the root account outside member-account SCPs; use CAM for member users and keys. |
| Global MFA enforcement | TCO general condition keys do not include `qcs:MFAPresent`. | Enforce MFA in CAM/identity operations and the organization's identity provider; apply it to sensitive CAM identities. |
| Deny only public security-group rules | The original `vpc:CidrIp` key is not a documented Tencent Cloud condition key. A hard deny would also block private rules. | Use CAM/service controls that support the request fields, security-group review, and network security governance. |
| Restrict resource sharing to an organization target | The original `organization:TargetUin` and `organization:ShareResource` mapping is not a documented TCO SCP condition contract. | Govern sharing through the relevant resource policy and an approval workflow. |
| Default CBS encryption toggle | `cbs:Encrypt` is not a documented condition key for the listed modification APIs, and disk encryption is established at disk creation. | Require encryption in the create workflow and audit existing disks with CBS/KMS tooling. |

This boundary is deliberate. A policy example is included only when its action, resource, condition key, and operator can be mapped to Tencent Cloud's documented policy model.
