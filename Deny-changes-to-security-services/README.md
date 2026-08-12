## Deny changes to security services

These policies are hard denies for the listed audit, monitoring, and security-service operations. Bind them to the protected departments or member accounts. Do not add an undocumented principal-tag exception; Tencent Cloud TCO SCP does not provide that condition key.

| Policy | Description |
|---|---|
| [Protect CloudAudit](deny-disabling-cloudaudit.json) | Denies deletion or modification of CloudAudit tracking operations. |
| [Protect Monitor alarms](deny-disabling-monitor-alarms.json) | Denies deletion or modification of listed alarm policies and notices. |
| [Protect CWP](deny-disabling-cwp.json) | Denies listed CWP disablement and destructive operations. |
| [Protect WAF](deny-disabling-waf.json) | Denies listed WAF deletion and protection-rule changes. |
| [Protect CSIP](deny-disabling-csip.json) | Denies listed CSIP destructive and service-closing operations. |
| [Protect selected CloudAudit trails](deny-modifying-cloudaudit-trails.json) | Denies changes to the configured CloudAudit resource prefix. |
