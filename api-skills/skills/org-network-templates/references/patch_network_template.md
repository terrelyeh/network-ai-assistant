- method: PATCH
- path: /orgs/{orgId}/network-templates/{templateId}

Update template name and/or description.

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
  "name": "Template 1 - Updated",
  "description": "Updated description"
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | false | New template name. |
| description | string | false | New note/description (max 255 chars recommended). |

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

- Send only fields to change; omit unchanged fields.
- Resolve `templateId` from a fresh `get_network_templates` result to avoid stale ids.
