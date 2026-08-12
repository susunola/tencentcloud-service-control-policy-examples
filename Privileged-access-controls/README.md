## Privileged access controls

These policies use hard denies. Tencent Cloud TCO SCP does not support the AWS-style principal-tag exception pattern used by the original files. To create an exception, bind the policy only to the departments or member accounts that should be protected, and keep privileged administration in a separately governed node.

| Policy | Description |
|---|---|
| [Deny member leave operations](deny-member-leave-organization.json) | Denies the documented organization APIs used to leave or remove members. |
| [Protect selected CAM roles](deny-modifications-to-specific-cam-roles.json) | Denies changes to roles matching the configured resource prefix. |
| [Protect critical CAM user operations](deny-critical-cam-user-actions.json) | Denies creation, modification, and deletion of sensitive CAM users and keys, plus password-rule changes. |
| [Protect billing settings](deny-billing-modification.json) | Denies changes to billing and account settings covered by the listed actions. |
| [Protect identity federation](deny-unwarranted-identity-federation.json) | Denies changes to SAML and OIDC identity providers. |
