## Service-specific controls

These examples use service actions, resource paths, and documented service-level condition keys. Hard-deny examples have no principal-tag exceptions; control the blast radius through TCO binding scope.

### COS

| Policy | Description |
|---|---|
| [Protect COS buckets and objects](COS/deny-deleting-cos-buckets-or-objects.json) | Denies deletion of a configured bucket and its objects. |
| [Deny public COS ACLs](COS/deny-public-cos-buckets.json) | Denies public and authenticated-read bucket/object ACLs. |
| [Protect sensitive bucket encryption settings](COS/deny-modifying-encryption-on-sensitive-buckets.json) | Denies changes to encryption settings for a configured bucket prefix. |
| [Deny public bucket ACLs](COS/deny-public-bucket-acl.json) | Denies public ACL headers on bucket creation and bucket ACL updates. |

### CVM

| Policy | Description |
|---|---|
| [Restrict CVM instance types](CVM/restrict-instance-types.json) | Denies `RunInstances` when `cvm:instance_type` is outside the approved list. |
| [Protect CVM instances](CVM/deny-terminating-instances.json) | Denies termination and stop operations for the configured instance scope. |
| [Protect image sharing](CVM/deny-disabling-block-public-access-on-images.json) | Denies the listed image sharing and attribute changes. |

### CAM

| Policy | Description |
|---|---|
| [Protect selected CAM roles](CAM/deny-modifications-to-specific-roles.json) | Denies changes to roles matching the configured resource prefix. |
| [Protect attached CAM policies](CAM/deny-deleting-attached-policies.json) | Denies deletion, modification, and detachment actions in the listed scope. |

### VPC

| Policy | Description |
|---|---|
| [Deny public VPC connectivity changes](VPC/deny-public-vpc-connectivity.json) | Denies the listed NAT, VPN, internet-gateway, and address-association operations. |
| [Protect VPC flow logs](VPC/deny-vpc-flow-log-deletion.json) | Denies deletion and modification of VPC flow-log configuration. |
