- method: POST
- path: /orgs/{orgId}/network-groups

Create a network group under the organization.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Organization id (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "name": "Branch Group",
  "network_ids": [
    "605d520c1e2fa05f5712603e",
    "605d520c1e2fa05f5712603f"
  ]
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | true | Group name. |
| network_ids | array[string] | true | Member network ids. Resolve from `get_hierarchy_views.networks[].id`. |

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

- Use `network_ids` key in payload.
- Resolve valid network ids from hierarchy views to avoid invalid membership ids.
