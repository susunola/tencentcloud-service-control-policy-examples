## Protect cloud platform resources

These policies are hard denies. Tencent Cloud TCO SCP does not support the original principal-tag exception conditions, so exceptions must be designed through policy binding scope rather than an invented condition key.

| Policy | Description |
|---|---|
| [Protect VPC resources](deny-deleting-vpc-resources.json) | Denies deletion of VPC and selected network resources. |
| [Protect KMS keys](deny-deleting-kms-keys.json) | Denies deletion, disabling, and scheduled deletion of selected KMS keys. |
| [Protect selected SCF functions](deny-modifying-specific-scf-functions.json) | Denies changes to functions matching the configured resource prefix. |
| [Protect CLB resources](deny-unwanted-clb-deletion.json) | Denies deletion and selected modification of CLB resources. |

CBS encryption is intentionally not represented as an SCP condition. Encryption is established during disk creation and `cbs:Encrypt` is not a documented condition key for the removed modification policy. See [UNSUPPORTED.md](../UNSUPPORTED.md).
