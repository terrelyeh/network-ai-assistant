- method: GET
- path: /orgs/{orgId}/network-groups

List network groups under the organization.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Organization id (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body

(EMPTY)

### Response Body Example

```json
{
  "groups": [
    {
      "id": "66f04f4439e1dc784fa13e0a",
      "name": "Branch Group",
      "network_ids": [
        "605d520c1e2fa05f5712603e",
        "605d520c1e2fa05f5712603f"
      ]
    }
  ]
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| groups | array[object] | Network group list. |

### groups[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Network group id. |
| name | string | Network group name. |
| network_ids | array[string] | Member network ids. |

### Usage Notes

- Use `groups[].id` as `groupId` for patch/delete.
- Candidate mapping can be normalized to `org_network_group_candidates` (`group_id`, `name`) for name-to-id resolution.
