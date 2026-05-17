- method: POST
- path: /orgs/{orgId}/memberships/{userId}/invitations

Sends org invitation email. Query parameter `url` is supported for redirect behavior.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization id. |
| userId | string | Target user id to re-send invitation. |
