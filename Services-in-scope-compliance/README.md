## Compliance controls

This category contains one explicit allow-boundary example. It must replace an unrestricted allow policy at the target organization node; attaching it beside `FullQcloudAccess` does not narrow permissions.

| Policy | Description |
|---|---|
| [Allow selected actions with required tags](allow-actions-with-required-tags.json) | Allows selected create operations only when `qcs:request_tag` contains the configured `cost-center&[COST_CENTER]` value. Expand the action/resource set deliberately and test each API because request-tag support is service-specific. |

MFA enforcement is not included because TCO SCP does not document a `qcs:MFAPresent` condition key. See [UNSUPPORTED.md](../UNSUPPORTED.md) for the boundary and alternatives.
