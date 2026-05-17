- method: GET
- path: /orgs/{orgId}/network-templates/candidates

Return candidate source networks for template creation.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). Resolve from `get_user_orgs`. |

### Query Parameters

(EMPTY)

### Request Body

(EMPTY)

### Response Body Example

```json
{
  "networks": [
    {
      "id": "605d520c1e2fa05f5712603e",
      "name": "HQ Network"
    }
  ]
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| networks | array[object] | Candidate source networks that satisfy template constraints. |

### networks[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Candidate network id. |
| name | string | Candidate network name. |

### Usage Notes

- Always call this API before `create_network_template`.
- Map selected network name to `org_network_template_candidates.network_id`; do not assume any network is eligible if missing from this list.
