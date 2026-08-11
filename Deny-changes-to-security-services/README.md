## 禁止修改安全服务

限制成员账号禁用用于监管、合规、操作审计和风险审计的安全工具。

| 策略 | 说明 |
|------|------|
|[禁止关闭操作审计](deny-disabling-cloudaudit.json)|限制删除或修改 CloudAudit（操作审计）的跟踪配置。|
|[禁止关闭或修改云监控告警](deny-disabling-monitor-alarms.json)|限制删除或修改关键告警策略和通知。|
|[禁止关闭主机安全](deny-disabling-cwp.json)|限制卸载主机安全客户端、关闭专业版或修改告警配置。|
|[禁止关闭 Web 应用防火墙](deny-disabling-waf.json)|限制删除 WAF 实例、修改域名防护模式或删除自定义规则。|
|[禁止关闭云安全中心](deny-disabling-csip.json)|限制删除风险、修改风险状态、删除资产或关闭云安全中心服务。|
|[禁止修改指定操作审计跟踪](deny-modifying-cloudaudit-trails.json)|限制对安全或合规团队所需的特定 CloudAudit 跟踪进行修改操作。|
