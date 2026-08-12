<p align="center">
  <a href="README.md">English</a> &nbsp;|&nbsp;
  <b>简体中文</b>
</p>

# 腾讯云服务管控策略（SCP）示例

## 范围与安全

本仓库面向**腾讯云集团账号管理（TCO）服务管控策略**，不是 AWS Organizations SCP 的移植版。所有文件都是参考模板，不代表已在每个腾讯云账号和地域中完成真实环境验证。

在绑定到生产组织前，必须先在独立部门或成员账号中测试。拒绝策略可能阻断控制台操作、自动化流程、服务相关角色操作和应急响应。

TCO SCP 定义组织级权限边界，不替代 CAM 身份策略或资源策略。腾讯云会先按组织层级评估 SCP，再评估 CAM；每一层都需要命中适用的允许策略才能继续向上评估。需要保留广泛权限时，保留系统策略 `FullQcloudAccess`，再叠加拒绝型管控策略。如果用自定义允许策略替换它，该策略就是允许边界，必须覆盖该层所需的全部操作。

服务相关角色不受 TCO SCP 约束。本仓库不提供根账号控制和 MFA 强制策略，因为腾讯云没有为 TCO SCP 提供 AWS 风格的根用户/MFA 条件键。

## 本仓库使用的策略语法

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "deny",
      "action": ["service:ActionName"],
      "resource": ["qcs::service:region:account:resource"],
      "condition": {
        "string_equal": {
          "qcs:resource_tag": "key&value"
        }
      }
    }
  ]
}
```

| 字段 | 说明 |
|---|---|
| `version` | 固定为 `"2.0"`。 |
| `effect` | 防护策略使用 `deny`；标签约束示例唯一使用 `allow`，它是允许边界。 |
| `action` | 腾讯云 CAM 操作名，例如 `cvm:TerminateInstances`。本仓库不使用也不支持 `not_action`。 |
| `resource` | `*` 或六段式 QCS 资源。本仓库不使用也不支持 `not_resource`。 |
| `condition` | 可选。只使用所选操作对应的官方通用条件键或服务级条件键。 |

官方通用条件键为 `qcs:current_time`、`qcs:ip`、`qcs:resource_tag` 和 `qcs:request_tag`。本仓库的服务级示例使用 `cvm:region`、`cvm:instance_type`、`vpc:region` 和 `cos:x-cos-acl`。条件键区分大小写。

## 策略类别

| 类别 | 数量 | 说明 |
|---|---:|---|
| [特权访问控制](Privileged-access-controls/README.md) | 5 | 保护组织成员关系、CAM 用户、角色、账单和身份联合。 |
| [地域管控](Region-controls/README.md) | 1 | 限制 CVM 和 VPC 操作只能使用批准地域。 |
| [禁止修改安全服务](Deny-changes-to-security-services/README.md) | 6 | 保护 CloudAudit、WAF、CWP、CSIP 和 Monitor。 |
| [保护云平台资源](Protect-cloud-platform-resource/README.md) | 4 | 保护 VPC、KMS、SCF 和 CLB 资源。 |
| [敏感数据保护](Sensitive-data-protection/README.md) | 2 | 保护 COS 数据和公开 ACL。 |
| [服务专项管控](Service-specific-controls/README.md) | 11 | COS、CVM、CAM 和 VPC 管控。 |
| [合规管控](Services-in-scope-compliance/README.md) | 1 | 对指定创建操作提供带标签的允许边界。 |

## 建议先看这些策略

| 策略 | 作用 |
|---|---|
| [禁止成员退出操作](Privileged-access-controls/deny-member-leave-organization.json) | 阻止覆盖到的成员退出或被移出集团组织。 |
| [限制 CVM 和 VPC 地域](Region-controls/deny-unapproved-cvm-and-vpc-regions.json) | 拒绝服务级地域条件不在批准列表中的 CVM/VPC 请求。 |
| [保护安全服务](Deny-changes-to-security-services/README.md) | 防止操作审计、监控和安全控制被修改。 |
| [保护敏感 COS 存储桶](Service-specific-controls/COS/deny-deleting-cos-buckets-or-objects.json) | 阻止删除指定存储桶及其对象。 |
| [要求带标签的允许边界](Services-in-scope-compliance/allow-actions-with-required-tags.json) | 仅允许请求带有指定标签值的创建操作。应在目标层级替换无限制允许策略，不要与其叠加。 |

## 校验

```bash
python3 tests/test_policies.py
```

校验器覆盖 JSON 编码、结构、腾讯云专属元素、官方条件键和操作符、QCS 形状、策略长度、占位符、重复操作、README 引用和仓库完整性。遇到 AWS 风格的 `not_action`、`not_resource`、PrincipalTag、根用户、MFA 或 ARN 构造会直接失败。

## 已知能力边界

请阅读 [UNSUPPORTED.md](UNSUPPORTED.md)。其中列出因腾讯云 TCO 无法用官方 SCP/CAM 模型安全表达而移除的控制项。涉及身份主体、MFA、公网 IP 请求参数或组织外共享目标的控制，应使用对应 CAM 策略、资源策略、产品控制或组织外治理流程，不要伪造 SCP 条件键。

## 相关文档

| 文档 | 链接 |
|---|---|
| TCO 服务管控策略概述 | https://www.tencentcloud.com/document/product/1031/51871 |
| 开启服务管控策略 | https://cloud.tencent.com/document/product/850/83576 |
| CAM 策略语法 | https://cloud.tencent.com/document/product/598/10604 |
| CAM 条件键和条件运算符 | https://cloud.tencent.com/document/product/598/10608 |
| CVM 条件键 | https://cloud.tencent.com/document/product/454/10313 |
| COS 条件键 | https://cloud.tencent.com/document/product/239/71306 |
| 标签约束策略示例 | https://cloud.tencent.com/document/api/1081/104657 |

## 贡献

提交 PR 前请运行 `python3 tests/test_policies.py`。新增策略时，请为每个条件键引用腾讯云 API 或 CAM 文档，并说明影响范围、占位符、测试范围和回滚方式。

## 许可证

MIT-0 License — 详见 [LICENSE](LICENSE)。
