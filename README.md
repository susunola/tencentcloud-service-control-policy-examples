# Tencent Cloud Service Control Policy Examples

# 腾讯云服务管控策略（SCP）示例

<br>

---

<p align="center">
  <strong>中文</strong> &nbsp;|&nbsp; <a href="#-english">English</a>
</p>

---

## 概述

**本仓库中的服务管控策略仅供参考。** 不建议在未充分测试策略对账号影响的情况下直接绑定 SCP。在准备好实施策略后，建议先在独立的组织或部门中进行测试，确认无误后再逐步推广到更广泛的部门。

[服务管控策略（Service Control Policies, SCP）](https://cloud.tencent.com/document/product/850/10540) 是腾讯云集团账号管理提供的一种粗粒度管控手段。SCP 不直接授予权限——管理员仍须为账号中的 CAM 子用户或角色绑定 [身份策略](https://cloud.tencent.com/document/product/598/10601) 或 [资源策略](https://cloud.tencent.com/document/product/598/10602) 才能实际授予权限。有效权限是 SCP 与身份策略/资源策略的逻辑交集。

当 SCP 绑定到集团账号的组织、部门或成员时，会为所有成员的权限设置一个最大可用权限边界。了解 [SCP 评估逻辑](https://cloud.tencent.com/document/product/850/10540) 有助于编写得到预期结果的策略。

建议根据**功能、合规要求或共通的管控需求**来组织成员，而非直接映射企业的汇报结构。如果你刚开始搭建集团账号，请参考 [集团账号最佳实践](https://cloud.tencent.com/document/product/850/10541)。

### 策略语法

```json
{
    "version": "2.0",
    "statement": [
        {
            "effect": "deny",
            "action": ["service:ActionName"],
            "resource": ["qcs::service:region:account:resource"],
            "condition": { }
        }
    ]
}
```

| 字段 | 说明 |
|------|------|
| `version` | 策略版本，固定为 `"2.0"` |
| `effect` | `"deny"`（显式拒绝）或 `"allow"`（允许） |
| `action` | 格式 `服务缩写:API操作名`，如 `cvm:TerminateInstances`。支持通配符 `*` 和 `not_action` |
| `resource` | 六段式 QCS 格式 `qcs::服务:地域:账号:资源`，或 `*`。支持 `not_resource` |
| `condition` | 可选，指定策略生效条件。支持字符串/数值/日期/IP/布尔/空值操作符 |

> **注意**：本仓库中的 SCP 示例采用 **拒绝列表策略（Deny List Strategy）**，意味着你还需要为组织实体绑定允许访问的策略（例如系统预设的 `FullQcloudAccess`），并继续通过身份策略或资源策略为子用户/角色授予适当权限。

### 策略类别

| 类别 | 数量 | 说明 |
|------|------|------|
| [特权访问控制](Privileged-access-controls/README.md) | 7 | 确保角色和应用只被授予最小权限 |
| [地域管控](Region-controls/README.md) | 1 | 禁止使用未批准的地域 |
| [禁止修改安全服务](Deny-changes-to-security-services/README.md) | 6 | 保护 CloudAudit/WAF/CWP/CSIP/Monitor 等安全工具不被关闭 |
| [保护云平台资源](Protect-cloud-platform-resource/README.md) | 5 | 保护 VPC/KMS/SCF/CBS/CLB 等核心资源不被删除或修改 |
| [敏感数据保护](Sensitive-data-protection/README.md) | 4 | 防止 COS 公开访问、安全组全量开放、资源外泄 |
| [服务专项管控](Service-specific-controls/README.md) | 11 | COS/CVM/CAM/VPC 等专项服务策略 |
| [合规管控](Services-in-scope-compliance/README.md) | 2 | MFA 强制、标签合规 |

### 入门推荐

| # | 策略 | 作用 |
|---|------|------|
| 1 | [禁止成员退出集团组织](Privileged-access-controls/deny-member-leave-organization.json) | 防止成员账号脱离集团管控 |
| 2 | [仅允许使用已批准的地域](Region-controls/deny-access-based-on-requested-region.json) | 地域白名单，阻止在未授权地域创建资源 |
| 3 | [防止成员账号管理根账号凭证](Privileged-access-controls/prevent-root-credentials-management.json) | 集中管控根账号访问密钥和登录配置 |
| 4 | [禁止根用户执行操作](Privileged-access-controls/deny-root-user-actions-except-exceptions.json) | 仅允许根用户执行特定例外操作 |
| 5 | [禁止修改安全服务](Deny-changes-to-security-services/README.md) | 保护 CloudAudit、WAF、CWP 等不被成员账号停用 |
| 6 | [保护敏感 COS 存储桶](Service-specific-controls/COS/deny-deleting-cos-buckets-or-objects.json) | 防止误删或恶意删除关键数据 |

### 测试

```bash
cd tests
python3 test_policies.py
```

测试覆盖五层共 831 项断言：基础语法（编码/BOM/空格）、结构完整性、语义正确性（服务前缀/条件操作符/QCS 格式/无 AWS 引用）、一致性（README 交叉引用/文件完整性）、安全最佳实践（占位符格式/not_action 约束/缩进）。

---

## 相关文档

| 文档 | 链接 |
|------|------|
| SCP 概述 | https://cloud.tencent.com/document/product/850/10540 |
| CAM 策略语法 | https://cloud.tencent.com/document/product/598/10603 |
| 集团账号管理 | https://cloud.tencent.com/document/product/850/10539 |
| 访问管理最佳实践 | https://cloud.tencent.com/document/product/598/10592 |

## 贡献

Bug report 和 PR 欢迎。提交前请运行测试套件。

## 许可证

MIT-0 License — 详见 [LICENSE](LICENSE)。

---

<br>
<br>
<br>

---

## 🇬🇧 English

### Overview

**The SCP examples in this repository are for reference only.** Do not attach SCPs without thoroughly testing the impact on accounts. Test in a separate organization or OU before deploying to broader scopes.

[Service Control Policies (SCPs)](https://www.tencentcloud.com/document/product/1031/51871) are coarse-grained guardrails in Tencent Cloud Organization (TCO). They do not grant permissions — administrators must still attach [identity-based](https://www.tencentcloud.com/document/product/598/10601) or [resource-based](https://www.tencentcloud.com/document/product/598/10602) policies. Effective permissions are the **logical intersection** of the SCP and the identity/resource policy.

Organize accounts by **function, compliance requirement, or common controls** — not by org-chart hierarchy. For a deep-dive on SCP evaluation, see [SCP Evaluation Logic](https://www.tencentcloud.com/document/product/1031/51871).

### Policy Syntax

Uses standard Tencent Cloud CAM policy syntax:

```json
{
    "version": "2.0",
    "statement": [
        {
            "effect": "deny",
            "action": ["service:ActionName"],
            "resource": ["qcs::service:region:account:resource"],
            "condition": { }
        }
    ]
}
```

| Field | Description |
|-------|-------------|
| `version` | Always `"2.0"` |
| `effect` | `"deny"` (explicit deny) or `"allow"` |
| `action` | `service:ActionName`, e.g. `cvm:TerminateInstances`. Supports `*` and `not_action` |
| `resource` | Six-segment QCS format `qcs::service:region:account:resource`, or `*`. Supports `not_resource` |
| `condition` | Optional. Supports string/numeric/date/IP/boolean/null operators |

> **Note**: Examples use a **deny-list strategy** — attach an allow policy (e.g. `FullQcloudAccess`) alongside, and grant permissions via identity/resource policies.

### Categories

| Category | Count | Purpose |
|----------|-------|---------|
| [Privileged Access Controls](Privileged-access-controls/README.md) | 7 | Least-privilege enforcement for roles and apps |
| [Region Controls](Region-controls/README.md) | 1 | Block unapproved regions |
| [Deny Changes to Security Services](Deny-changes-to-security-services/README.md) | 6 | Protect CloudAudit, WAF, CWP, CSIP, Monitor |
| [Protect Cloud Platform Resource](Protect-cloud-platform-resource/README.md) | 5 | Guard VPC/KMS/SCF/CBS/CLB from deletion |
| [Sensitive Data Protection](Sensitive-data-protection/README.md) | 4 | Prevent public COS, open SGs, data exfiltration |
| [Service-Specific Controls](Service-specific-controls/README.md) | 11 | COS/CVM/CAM/VPC service-level policies |
| [Services in Scope Compliance](Services-in-scope-compliance/README.md) | 2 | MFA enforcement, tagging compliance |

### Top SCPs to Start With

| # | Policy | Goal |
|---|--------|------|
| 1 | [Deny member accounts from leaving the organization](Privileged-access-controls/deny-member-leave-organization.json) | Prevent account detachment from TCO |
| 2 | [Only allow approved regions](Region-controls/deny-access-based-on-requested-region.json) | Region allowlist |
| 3 | [Prevent root credentials management](Privileged-access-controls/prevent-root-credentials-management.json) | Centralize root key and login control |
| 4 | [Deny root user actions except exceptions](Privileged-access-controls/deny-root-user-actions-except-exceptions.json) | Restrict root to specific operations |
| 5 | [Deny changes to security services](Deny-changes-to-security-services/README.md) | Guardrails for CloudAudit, WAF, CWP |
| 6 | [Protect sensitive COS buckets](Service-specific-controls/COS/deny-deleting-cos-buckets-or-objects.json) | Block accidental/malicious deletion |

### Testing

```bash
cd tests
python3 test_policies.py
```

831 assertions across 5 levels: syntax (encoding/BOM/whitespace), structural (required keys, mutual exclusion), semantic (service prefixes, condition operators, QCS format, no AWS refs), consistency (README cross-reference, file completeness), and best practices (placeholder format, not_action safety, indentation).

### Documentation

| Resource | Link |
|----------|------|
| SCP Overview | https://www.tencentcloud.com/document/product/1031/51871 |
| CAM Policy Syntax | https://www.tencentcloud.com/document/product/598/10603 |
| TCO Management | https://www.tencentcloud.com/document/product/1031 |
| CAM Best Practices | https://www.tencentcloud.com/document/product/598/10592 |

### Contributing

Bug reports and pull requests welcome. Run the test suite before submitting.

### License

MIT-0 License — see [LICENSE](LICENSE).
