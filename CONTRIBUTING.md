# 贡献指南

感谢你考虑为腾讯云服务管控策略示例仓库做出贡献！

## 如何贡献

### 提交策略示例

1. 确保策略语法符合 [腾讯云 CAM 策略语法](https://cloud.tencent.com/document/product/598/10603) 规范
2. 策略必须采用 **拒绝列表策略（Deny List）** 方式，即 `"effect": "deny"`
3. 版本号使用 `"version": "2.0"`
4. 资源描述使用腾讯云六段式格式（`qcs::服务:地域:账号:资源`）或 `"*"`
5. 将策略文件放在合适的分类目录下
6. 更新对应目录的 `README.md` 添加策略说明

### 测试

提交前请运行测试：

```bash
cd tests
python3 test_policies.py
```

所有 JSON 文件必须是合法的 JSON，且必须包含必需的策略字段（version、statement、effect、action、resource）。

### Pull Request 流程

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 确保所有测试通过
5. 创建 Pull Request 并描述更改内容

### 编码规范

- JSON 文件使用 2 空格缩进
- 策略描述使用中文
- 资源占位符使用 `[PLACEHOLDER]` 格式
- 文件命名使用小写字母和连字符（kebab-case）

## 安全

如果你发现安全相关问题，请勿提交公开 Issue，而是通过安全渠道联系维护者。
