- method: POST
- path: /orgs/{orgId}/backups/{backupId}/restoration

Restore network settings from a selected backup.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| backupId | string | Backup id from `get_org_backups.backups[].id`. |

### Query Parameters

(EMPTY)

### Request Body

(EMPTY)

### Response Body Example

```json
{
  "code": 200,
  "message": "OK",
  "hierarchy_view_id": "59d72645g799c000126e38e",
  "network_id": "59d72645g799c000126e388"
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code (`200` on success). |
| message | string | Result message. |
| hierarchy_view_id | string | Restored network's hierarchy view id. |
| network_id | string | Restored network id. |

### Usage Notes

- `backupId` must be backup id, not network id.
