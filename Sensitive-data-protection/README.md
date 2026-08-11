## 敏感数据保护

保护不应被公开访问或意外删除的敏感数据。

| 策略 | 说明 |
|------|------|
|[禁止设置 COS 存储桶公开 ACL](deny-public-cos-bucket-acl.json)|禁止将 COS 存储桶或对象设置为公开读取或公开读写。|
|[禁止删除 COS 存储桶或对象](deny-deleting-cos-buckets-or-objects.json)|禁止删除指定的敏感 COS 存储桶或其中的对象。建议将 `"Resource":"*"` 替换为特定的敏感存储桶资源。|
|[禁止开放全量安全组规则](deny-public-security-group-rules.json)|禁止创建 0.0.0.0/0 的安全组入站规则，防止资源直接暴露于公网。|
|[禁止向组织外共享资源](deny-unwarranted-resource-sharing.json)|禁止向集团组织外部的 UIN 共享资源。|
