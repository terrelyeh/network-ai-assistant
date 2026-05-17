- method: PATCH
- path: /orgs/{orgId}/backups/{backupId}

Update backup protection/status/name/description.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| backupId | string | Backup id from `get_org_backups.backups[].id`. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "is_protected": true
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| is_protected | boolean | false | Protect/unprotect backup. |
| is_updated | boolean | false | Re-backup using current network settings (`true`). |
| name | string | false | New backup name. |
| description | string | false | New backup description. |

### Response Body Example

```json
{
  "code": 200,
  "message": "OK",
  "snapshot_time": 1709541621000
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code (`200` on success). |
| message | string | Result message. |
| snapshot_time | integer | Snapshot timestamp when applicable. |

### Usage Notes

- Send only fields for one intended action (protect, re-backup, or rename/description).
- Resolve `backupId` only from `get_org_backups` response.
