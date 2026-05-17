- method: GET
- path: /orgs/{orgId}/network-templates

Return configuration templates under the organization.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). Resolve from `get_user_orgs`. |

### Query Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| from | integer | false | 0 | Pagination start index. |
| count | integer | false | 10 | Number of returned templates. |
| order | string | false | + | Sort order: `+` (asc) or `-` (desc). |
| sort | string | false | name | Sort field: `name`, `modified_time`, `modified_by`. |

### Request Body

(EMPTY)

### Response Body Example

```json
{
  "size": 1,
  "templates": [
    {
      "id": "615548211ac508f7e722510e",
      "name": "Template 1",
      "modified_time": 1709541621000,
      "modified_by": "user@example.com",
      "config_summary": {
        "is_network_config": true,
        "is_switch_config": true,
        "is_switch_extender_config": false,
        "is_pdu_config": false
      },
      "description": "Template 1 Description",
      "applied_network_ids": [
        "605d520c1e2fa05f5712603e"
      ]
    }
  ]
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| size | integer | Total number of templates in response scope. |
| templates | array[object] | List of template objects. |

### templates[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Template id. |
| name | string | Template name. |
| modified_time | integer | Last modified timestamp in milliseconds. |
| modified_by | string | User who last modified this template. |
| config_summary | object | Template capability summary. |
| description | string | Template note/description. |
| applied_network_ids | array[string] | Network ids currently applied to this template. |

### Usage Notes

- Use this API before update/delete/apply flows to resolve exact `templateId` (`templates[].id`).
- Successful results can be normalized to `org_configuration_template_candidates` (`template_id`, `name`) for downstream operations.
