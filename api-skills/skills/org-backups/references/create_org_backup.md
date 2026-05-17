- method: POST
- path: /orgs/{orgId}/backups

Create a backup for a target network in the organization.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "name": "Backup",
  "hierarchy_view_id": "59d72645g799c000126e38e",
  "network_id": "59d72645g799c000126e388",
  "is_protected": true,
  "description": ""
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | true | Backup display name. |
| hierarchy_view_id | string | true | Hierarchy view id. |
| network_id | string | true | Network id to back up. |
| description | string | false | Optional description. |
| is_protected | boolean | false | Whether backup is protected from rotation/deletion policies. |

### Response Body Example

```json
{
  "code": 200,
  "message": "OK",
  "id": "615548211ac508f7e722510e",
  "name": "Backup",
  "network_name": "HQ Network",
  "is_protected": true,
  "creator": "user@example.com",
  "description": "",
  "created_time": 1709541621000,
  "snapshot_time": 1709541621000,
  "modified_time": 1709541621000
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code (`200` on success). |
| message | string | Result message. |
| id | string | Created backup id. |
| name | string | Backup name. |
| network_name | string | Target network name. |
| is_protected | boolean | Protected flag. |
| creator | string | Backup creator. |
| description | string | Backup description. |
| created_time | integer | Creation timestamp in milliseconds. |
| snapshot_time | integer | Snapshot timestamp in milliseconds. |
| modified_time | integer | Last modified timestamp in milliseconds. |
