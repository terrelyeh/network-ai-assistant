- method: PATCH
- path: /orgs/{orgId}/networks/memberships

Invite users to networks, update role, or remove role membership mapping.

### Request Body Example

```json
{
  "emails": [
    "senao@senao.com",
    "senaocloud@senao.com"
  ],
  "networks": [
    {
      "id": "553f65154ec153e59cdc84ba",
      "hierarchy_view_id": "fbdc18a101b15b479a0664a5",
      "role": "admin"
    }
  ]
}
```

### Request Body Schema

| Field | Type | Description |
|---|---|---|
| emails | array[string] | Target user emails for batch operation. |
| networks | array[object] | Network role assignment list. |

### Input Validation Notes (Pre-check Before API Call)

- Validate all values in `emails[]` using the same rules as org membership create:
  - exactly one `@`
  - non-empty local part and domain part
  - domain contains at least one `.`
  - no spaces
- If any email is invalid, stop early and do not call API.

### networks[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Target network id. |
| hierarchy_view_id | string | Hierarchy view id that owns the network. |
| role | string | Network role (`admin`, `viewer`, `frontdesk`). |

### Response Body Example

```json
[
  {
    "email": "senao@senao.com",
    "networks": [
      {
        "code": 201,
        "message": "Created",
        "id": "553f65154ec153e59cdc84ba",
        "hierarchy_view_id": "fbdc18a101b15b479a0664a5",
        "inviter_email": "",
        "name": "",
        "role": "admin",
        "status": "pending",
        "created_time": 1540794509891,
        "modified_time": 1540794509891
      }
    ]
  }
]
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| email | string | Target user email for this result item. |
| networks | array[object] | Per-network operation results. |

### networks[] Result Item Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code for this network item (e.g., `201`). |
| message | string | Result message. |
| id | string | Target network id. |
| hierarchy_view_id | string | Hierarchy view id used in operation. |
| inviter_email | string | Inviter email (if available). |
| name | string | Network or user name (if available). |
| role | string | Resulting network role. |
| status | string | Membership status (e.g., `pending`, `active`). |
| created_time | integer | Creation timestamp in milliseconds. |
| modified_time | integer | Last update timestamp in milliseconds. |
