- method: DELETE
- path: /orgs/{orgId}/network-templates

Delete one or more configuration templates.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). Resolve from `get_user_orgs`. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
[
  "59d72645g799c000126e388",
  "59d72645g799c000126e389"
]
```

### Request Body Schema

Root payload must be `array[string]` of template ids.

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

- Body root must be the JSON array itself. Do **not** wrap with keys such as `templateIds` or `ids`.
- Id source: `get_network_templates.templates[].id` (or `org_configuration_template_candidates.template_id`).
