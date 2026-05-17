- method: GET
- path: /orgs/{orgId}/memberships/overall

Returns overall memberships across org and networks.

### Response Body Example

```json
[
  {
    "id": "a820059319c955439f3d8634",
    "name": "senao",
    "email": "root@senao.com",
    "last_login_time": 1521535457869,
    "status": "active",
    "org": {
      "id": "12e3r65154ec153e59cdc2r12ra",
      "name": "org 1",
      "role": "admin",
      "status": "active",
      "created_time": 1521535457869,
      "modified_time": 1521535457869
    },
    "networks": [
      {
        "id": "553f65154ec153e59cdc84ba",
        "hierarchy_view_id": "fbdc18a101b15b479a0664a5",
        "name": "network 1",
        "role": "admin",
        "status": "active",
        "created_time": 1521535457869,
        "modified_time": 1521535457869
      }
    ]
  }
]
```

### Response Body Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | User identifier. |
| name | string | User display name. |
| email | string | User email. |
| last_login_time | integer | Last login timestamp in milliseconds. |
| status | string | User status (e.g., `active`, `pending`). |
| org | object | Organization-level membership information. |
| networks | array[object] | Network-level memberships for this user. |

### org Object Schema

| Field | Type | Description |
|---|---|---|
| id | string | Organization id. |
| name | string | Organization name. |
| role | string | Organization role (`admin` or `viewer`). |
| status | string | Org membership status. |
| created_time | integer | Creation timestamp in milliseconds. |
| modified_time | integer | Last update timestamp in milliseconds. |

### networks[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Network id. |
| hierarchy_view_id | string | Hierarchy view id owning the network. |
| name | string | Network name. |
| role | string | Network role (`admin`, `viewer`, `frontdesk`). |
| status | string | Network membership status. |
| created_time | integer | Creation timestamp in milliseconds. |
| modified_time | integer | Last update timestamp in milliseconds. |
