## 服务专项管控

针对特定腾讯云服务的管控策略。

### COS（对象存储）
| 策略 | 说明 |
|------|------|
|[禁止删除 COS 存储桶或对象](COS/deny-deleting-cos-buckets-or-objects.json)|禁止删除指定的敏感 COS 存储桶或其中的对象。|
|[禁止设置 COS 存储桶公开 ACL](COS/deny-public-cos-buckets.json)|禁止将 COS 存储桶或对象设置为公开读取或公开读写。|
|[禁止修改敏感存储桶的加密配置](COS/deny-modifying-encryption-on-sensitive-buckets.json)|禁止修改或删除敏感存储桶的加密配置。|
|[要求新存储桶禁用 ACL](COS/deny-acl-disablement-for-new-buckets.json)|要求所有新建存储桶使用私有 ACL。|

### CVM（云服务器）
| 策略 | 说明 |
|------|------|
|[限制 CVM 实例类型](CVM/restrict-instance-types.json)|只允许使用指定类型的 CVM 实例。|
|[禁止销毁 CVM 实例](CVM/deny-terminating-instances.json)|禁止非运维管理员销毁或关闭 CVM 实例。|
|[禁止关闭镜像公开访问限制](CVM/deny-disabling-block-public-access-on-images.json)|禁止修改镜像共享权限，防止镜像被公开。|

### CAM（访问管理）
| 策略 | 说明 |
|------|------|
|[禁止修改指定 CAM 角色](CAM/deny-modifications-to-specific-roles.json)|保护关键 CAM 角色不被删除或修改。|
|[禁止删除已绑定的策略](CAM/deny-deleting-attached-policies.json)|禁止删除或修改已绑定的 CAM 策略。|

### VPC（私有网络）
| 策略 | 说明 |
|------|------|
|[禁止创建公网连接](VPC/deny-public-vpc-connectivity.json)|限制创建 NAT 网关、VPN 网关、公网 IP 等公网连接资源。|
|[禁止删除 VPC 流日志](VPC/deny-vpc-flow-log-deletion.json)|限制删除或修改 VPC 流日志配置。|
