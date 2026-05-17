- method: GET
- path: /orgs/{orgId}/backups

Return backup list for the organization.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |

### Query Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| from | integer | false | 0 | Pagination start index. |
| count | integer | false | 10 | Number of returned backups. |
| order | string | false | + | Sort order: `+` or `-`. |
| sort | string | false | name | Sort field: `name`, `network_name`, `creator`, `created_time`, `snapshot_time`. |
| search | string | false | none | Search in backup name/network name/creator. |

### Request Body

(EMPTY)

### Response Body Example

```json
{
  "size": 1,
  "backups": [
    {
      "id": "615548211ac508f7e722510e",
      "name": "Backup",
      "is_protected": true,
      "network_id": "59d72645g799c000126e388",
      "network_name": "HQ Network",
      "creator": "user@example.com",
      "description": "",
      "created_time": 1709541621000,
      "snapshot_time": 1709541621000,
      "modified_time": 1709541621000
    }
  ]
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| size | integer | Returned backup count. |
| backups | array[object] | Backup list. |

### backups[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Backup id (use as `backupId`). |
| name | string | Backup name. |
| is_protected | boolean | Protected flag. |
| network_id | string | Related network id. |
| network_name | string | Related network name. |
| creator | string | Creator. |
| description | string | Description. |
| created_time | integer | Creation timestamp in milliseconds. |
| snapshot_time | integer | Snapshot timestamp in milliseconds. |
| modified_time | integer | Last modified timestamp in milliseconds. |

### Usage Notes

- Use `backups[].id` for `patch_org_backup`, `restore_network_backup`, and `delete_org_backups`.
