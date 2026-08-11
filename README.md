# 腾讯云服务管控策略（SCP）示例

**本仓库中的服务管控策略仅供参考。不建议在未充分测试策略对账号影响的情况下直接绑定 SCP。在准备好实施策略后，建议先在独立的组织或部门中进行测试，确认无误后再逐步推广到更广泛的部门。**

[服务管控策略（Service Control Policies, SCP）](https://cloud.tencent.com/document/product/850/10540) 是一种粗粒度的管控手段，不直接授予权限。管理员仍须为账号中的 CAM 子用户或角色绑定 [身份策略](https://cloud.tencent.com/document/product/598/10601) 或 [资源策略](https://cloud.tencent.com/document/product/598/10602)，才能实际授予权限。有效权限是 SCP 与身份策略/资源策略的逻辑交集。

当 SCP 绑定到集团账号的组织、部门或成员时，会为所有成员的权限设置一个最大可用权限边界。了解 [SCP 评估逻辑](https://cloud.tencent.com/document/product/850/10540) 有助于编写得到预期结果的策略。

建议根据功能、合规要求或共通的管控需求来组织成员，而非直接映射企业的汇报结构。如果你刚开始搭建集团账号，请参考 [集团账号最佳实践](https://cloud.tencent.com/document/product/850/10541)。

## 本仓库

示例策略按管控类型划分为不同类别。这些示例并非完整清单，你可以根据环境需求进行定制和扩展。

> **注意**：本仓库中的 SCP 示例采用 **拒绝列表策略（Deny List Strategy）**，意味着你还需要为组织实体绑定一个允许访问的策略（例如 `FullQcloudAccess`），并继续通过身份策略或资源策略为子用户/角色授予适当权限。

* **[特权访问控制](Privileged-access-controls/README.md)**：确保角色和应用只被授予完成预期功能所需的最小权限。

* **[地域管控](Region-controls/README.md)**：在多账号环境中禁止使用某些地域。

* **[禁止修改安全服务](Deny-changes-to-security-services/README.md)**：限制成员账号禁用用于监管、合规、操作审计和风险审计的安全工具。

* **[保护云平台资源](Protect-cloud-platform-resource/README.md)**：保护云资源不被修改或删除。

* **[敏感数据保护](Sensitive-data-protection/README.md)**：保护不应被公开访问或意外删除的敏感数据。

* **[服务专项管控](Service-specific-controls/README.md)**：针对特定腾讯云服务的管控策略。

## 推荐的入门 SCP

如果你刚开始实施 SCP，建议从以下策略入手：

* [禁止成员退出集团组织](Privileged-access-controls/deny-member-leave-organization.json)
* [仅允许使用已批准的地域](Region-controls/deny-access-based-on-requested-region.json)
* [防止成员账号管理根账号凭证](Privileged-access-controls/prevent-root-credentials-management.json)
* [禁止根用户执行操作（特定例外）](Privileged-access-controls/deny-root-user-actions-except-exceptions.json)
* [禁止修改安全服务](Deny-changes-to-security-services/README.md)
* [保护敏感 COS 存储桶](Service-specific-controls/COS/deny-deleting-cos-buckets-or-objects.json)

## 相关文档

* [服务管控策略（SCP）概述](https://cloud.tencent.com/document/product/850/10540)
* [腾讯云访问管理（CAM）策略语法](https://cloud.tencent.com/document/product/598/10603)
* [集团账号管理](https://cloud.tencent.com/document/product/850/10539)
* [访问管理最佳实践](https://cloud.tencent.com/document/product/598/10592)

## 策略语法

腾讯云服务管控策略使用 CAM 策略语法，格式如下：

```json
{
    "version": "2.0",
    "statement": [
        {
            "effect": "deny",
            "action": ["service:ActionName"],
            "resource": ["*"],
            "condition": { ... }
        }
    ]
}
```

- **version**：策略版本，固定为 `"2.0"`
- **effect**：`"deny"`（显式拒绝）或 `"allow"`（允许）
- **action**：格式为 `服务缩写:API操作名`，如 `cvm:TerminateInstances`
- **resource**：六段式格式 `qcs::服务:地域:账号:资源`，或使用 `*`
- **condition**：可选，指定策略生效条件

## 安全

详见 [CONTRIBUTING](CONTRIBUTING.md)。

## 许可证

本仓库使用 MIT-0 许可证。详见 [LICENSE](LICENSE) 文件。
