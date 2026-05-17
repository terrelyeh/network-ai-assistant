- method: DELETE
- path: /orgs/{orgId}/network-groups/{groupId}

Delete one network group.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Organization id (24-char hex). |
| groupId | string | Group id from `get_network_groups.groups[].id` or `org_network_group_candidates.group_id`. |

### Query Parameters

(EMPTY)

### Request Body

(EMPTY)

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

- Resolve `groupId` from a fresh group list to avoid deleting wrong/obsolete target.
