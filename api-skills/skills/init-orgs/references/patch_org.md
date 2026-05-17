- method: PATCH
- path: /orgs/{orgId}

Update organization-level settings.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). Resolve from `get_user_orgs`. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "ap_license_mode": "pro"
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| ap_license_mode | string | false | AP feature plan (`basic` or `pro`). |
| switch_license_mode | string | false | Switch feature plan (`basic` or `pro`). |
| gateway_license_mode | string | false | Gateway feature plan (`basic` or `pro`). |
| pdu_license_mode | string | false | PDU feature plan (`basic` or `pro`). |
| is_exposure_analysis_enable | boolean | false | Enable/disable exposure analysis. |

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

- Send only fields for the intended use case.
- Feature-plan changes and exposure-analysis changes should be separated when possible for clearer intent.
