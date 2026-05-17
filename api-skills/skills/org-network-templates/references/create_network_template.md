- method: POST
- path: /orgs/{orgId}/network-templates

Create a Configuration Template by cloning from an existing network.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). Resolve from `get_user_orgs`. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "name": "Template 1",
  "network_id": "59d72645g799c000126e388",
  "description": "Template 1 Description"
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | true | Template name. |
| network_id | string | true | Source network id. Use `org_network_template_candidates.network_id` after matching by network name. |
| description | string | false | Optional note/description. |

### Response Body Example

```json
{
  "code": 200,
  "message": "OK",
  "id": "615548211ac508f7e722510e",
  "name": "Template 1",
  "config_summary": {
    "is_network_config": true,
    "is_switch_config": true,
    "is_switch_extender_config": false,
    "is_pdu_config": false
  },
  "description": "Template 1 Description",
  "modified_time": 1709541621000,
  "modified_by": "user@example.com"
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code (`200` on success). |
| message | string | Result message (for example `OK`). |
| id | string | Created template id. |
| name | string | Template name. |
| config_summary | object | Template capability summary. |
| description | string | Template note/description. |
| modified_time | integer | Last modified timestamp in milliseconds. |
| modified_by | string | User who last modified this template. |

### config_summary Object Schema

| Field | Type | Description |
|---|---|---|
| is_network_config | boolean | Includes network-wide config. |
| is_switch_config | boolean | Includes switch config. |
| is_switch_extender_config | boolean | Includes switch extender config. |
| is_pdu_config | boolean | Includes PDU config. |

### Usage Notes

- Always call `get_network_template_candidates` first, then map user-selected source network name to `org_network_template_candidates.network_id`.
- Networks that violate template constraints are excluded from candidates (for example multiple gateways/switches/cameras/PDUs, or AP overriding network-wide settings).
