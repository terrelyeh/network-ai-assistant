- method: DELETE
- path: /orgs/{orgId}/backups

Delete backups in the organization.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
[
  "59d72645g799c000126e388"
]
```

### Request Body Schema

Root payload must be `array[string]` of backup ids.

### Response Body Example

```json
{
  "code": 200,
  "message": "OK"
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code (`200` on success). |
| message | string | Result message. |

### Usage Notes

- Root must be array itself (not object wrapper like `{"ids":[...]}`).
- Backup id source: `get_org_backups.backups[].id`.
