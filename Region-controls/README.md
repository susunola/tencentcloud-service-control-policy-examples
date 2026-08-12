## Region controls

Tencent Cloud does not provide a universal `qcs:RequestedRegion` condition key. This example uses the documented service-level keys `cvm:region` and `vpc:region`, so it covers CVM and VPC operations only.

Replace `[APPROVED_REGION_1]` and `[APPROVED_REGION_2]` with real region IDs such as `ap-guangzhou` and `ap-shanghai`. Add separate statements for other services using that service's documented region condition key. Treat operations without a usable region context as requiring separate validation.

| Policy | Description |
|---|---|
| [Deny unapproved CVM and VPC regions](deny-unapproved-cvm-and-vpc-regions.json) | Denies CVM and VPC requests whose service-level region is not in the approved list. |
