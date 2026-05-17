- method: GET
- path: /orgs/{orgId}/expired-devices-info

Return license-expiry summary for the organization.

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
  "earliest_expired_date": 1720828800000,
  "expired_devices_count": 3,
  "expired_devices_count_in_30_days": 2
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| earliest_expired_date | integer \| null | Earliest license expiration timestamp in milliseconds; `null` when no expiring devices. |
| expired_devices_count | integer | Number of already expired devices. |
| expired_devices_count_in_30_days | integer | Number of devices that will expire within 30 days. |

### Usage Notes

- Useful for dashboard/license warning use cases.
- Use with `get_user_orgs` result to select the correct `orgId`.
