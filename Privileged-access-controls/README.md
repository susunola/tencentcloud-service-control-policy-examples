## 特权访问控制示例

确保角色和应用只被授予完成预期功能所需的最小权限。

| 策略 | 说明 |
|------|------|
|[禁止成员退出集团组织](deny-member-leave-organization.json)|禁止受影响的账号中的用户或角色退出集团账号组织。|
|[防止成员账号管理根账号凭证](prevent-root-credentials-management.json)|集中管理成员账号的根用户访问权限。只允许具有特定标签的主账号或管理员角色对根账号凭证进行操作。|
|[禁止根用户执行操作（特定例外）](deny-root-user-actions-except-exceptions.json)|限制根用户执行日常操作，仅允许特定例外（如查看账号摘要、修改 COS 存储桶策略等）。|
|[禁止修改指定 CAM 角色](deny-modifications-to-specific-cam-roles.json)|限制账号中的 CAM 子用户修改特定 CAM 角色。|
|[禁止关键 CAM 用户操作](deny-critical-cam-user-actions.json)|限制创建和修改 CAM 子用户、访问密钥、登录配置和密码策略，只允许具有 `user-manager` 标签的角色执行。|
|[禁止修改账单信息](deny-billing-modification.json)|限制修改付款方式、税务偏好和联系信息。|
|[禁止未授权的身份联合创建和修改](deny-unwarranted-identity-federation.json)|限制创建和修改 SAML/OIDC 身份提供商，避免创建未授权的替代访问路径。|
