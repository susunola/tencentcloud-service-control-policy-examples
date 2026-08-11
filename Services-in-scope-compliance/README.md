## 合规管控

确保集团成员账号的操作符合合规要求。

| 策略 | 说明 |
|------|------|
|[要求 MFA 认证](require-mfa.json)|拒绝任何未通过 MFA 认证的操作请求。建议与各具体服务的允许策略配合使用，确保所有关键操作都需通过 MFA 验证。|
|[禁止不带指定标签创建资源](deny-actions-without-specific-tags.json)|要求创建 CVM、COS、VPC、CLB 等资源时必须附带 `cost-center` 等指定标签，以便成本归集和合规审计。|
