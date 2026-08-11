## 保护云平台资源

保护云资源不被修改或删除。

| 策略 | 说明 |
|------|------|
|[禁止删除 VPC 资源](deny-deleting-vpc-resources.json)|限制删除 VPC、子网、路由表、NAT 网关等网络核心资源。|
|[禁止删除或禁用 KMS 密钥](deny-deleting-kms-keys.json)|限制删除、禁用或计划删除 KMS 密钥，仅允许安全管理员操作。|
|[禁止修改指定云函数](deny-modifying-specific-scf-functions.json)|保护由平台方案部署的关键云函数不被修改或删除。|
|[禁止关闭默认 CBS 加密](deny-disabling-default-cbs-encryption.json)|要求所有云硬盘默认加密。注意：实施此策略前请确保已在账号中启用默认加密。|
|[禁止删除或修改负载均衡](deny-unwanted-clb-deletion.json)|限制删除或修改负载均衡实例，仅允许网络管理员操作。|
