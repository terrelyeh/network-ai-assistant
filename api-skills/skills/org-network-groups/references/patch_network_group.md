- method: PATCH
- path: /orgs/{orgId}/network-groups/{groupId}

Update network group name and/or member network list.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Organization id (24-char hex). |
| groupId | string | Group id from `get_network_groups.groups[].id` or `org_network_group_candidates.group_id`. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "name": "Branch Group - Updated",
  "network_ids": [
    "605d520c1e2fa05f5712603e"
  ]
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | false | New group name. |
| network_ids | array[string] | false | Full replacement member list after update (not delta). |

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

- `network_ids` is full replacement. To remove one network, fetch current group list then submit remaining ids.
- `network_ids: []` intentionally clears all member networks.
