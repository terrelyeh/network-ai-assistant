- method: POST
- path: /orgs/{orgId}/memberships

Invite users into an organization with org-level role.

### Request Body Example

```json
[
  {
    "email": "senao@senao.com",
    "role": "admin"
  },
  {
    "email": "root@senao.com",
    "role": "viewer"
  }
]
```

### Request Body Item Schema

| Field | Type | Description |
|---|---|---|
| email | string | Target user email. |
| role | string | Organization role (`admin` or `viewer`). |

### Input Validation Notes (Pre-check Before API Call)

- Validate each `email` before sending request.
- Minimal accepted format:
  - exactly one `@`
  - non-empty local part and domain part
  - domain contains at least one `.`
  - no spaces
- If any email is invalid, do not call API. Return a user-facing validation error directly.

### Response Body Example

```json
[
  {
    "code": 200,
    "message": "OK",
    "name": "",
    "role": "admin",
    "email": "senao@senao.com",
    "inviter_email": "",
    "status": "pending",
    "created_time": 1540794509891,
    "modified_time": 1540794509891
  },
  {
    "email": "root@senao.com",
    "message": "Conflict",
    "code": 409,
    "detailed_message": "User Role Is Already Existing"
  }
]
```

### Response Body Item Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code for this user invite (e.g., `200`, `409`). |
| message | string | Result message (`OK`, `Conflict`, etc.). |
| name | string | User display name (if available). |
| role | string | Assigned organization role. |
| email | string | Target user email. |
| inviter_email | string | Inviter email (if available). |
| status | string | Membership status (e.g., `pending`, `active`). |
| created_time | integer | Creation timestamp in milliseconds. |
| modified_time | integer | Last update timestamp in milliseconds. |
| detailed_message | string | Detailed error message when invite fails. |

### Planner Notes

- If a create membership item returns success (`code` in 2xx) with target role, avoid sending the same create request again with identical payload.
- Use the latest successful target role as source of truth for final user response wording.
