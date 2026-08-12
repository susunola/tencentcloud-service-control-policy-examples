## Sensitive data protection

Protect data that should not be public or deleted. The examples below use documented COS conditions or explicit QCS resources; they do not pretend to inspect unsupported VPC request parameters or sharing targets.

| Policy | Description |
|---|---|
| [Deny public COS ACLs](deny-public-cos-bucket-acl.json) | Denies bucket and object ACL requests that set public or authenticated-read ACLs. |
| [Protect selected COS buckets](deny-deleting-cos-buckets-or-objects.json) | Denies deletion of the configured bucket and its objects. Replace the `[APPID]`, `[BUCKET_TO_PROTECT]`, and region placeholders before use. |
