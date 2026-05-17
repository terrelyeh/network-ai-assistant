- method: POST
- path: /orgs/{orgId}/network-templates/{templateId}/apply

Apply template configuration to target networks.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). Resolve from `get_user_orgs`. |
| templateId | string | Template id from `get_network_templates.templates[].id` or `org_configuration_template_candidates.template_id`. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "network_ids": [
    "605d520c1e2fa05f5712603e"
  ]
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_ids | array[string] | true | Target network ids. Resolve from `get_hierarchy_views.networks[].id`, or use a full `network_ids` set from a network group. |

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

- `templateId` should be resolved from latest template list before apply.
- API accepts only `network_ids` in body; convert any group selection into explicit network id list before call.
