- method: POST
- path: /orgs/{orgId}/licenses/move

Move eligible licenses from source org to target org.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Source organization id (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "org_id": "5d3a70dfae4a1400010a36d7",
  "license_ids": [
    "69b7c4427621a6c1995f9a90"
  ]
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| org_id | string | true | Target organization id (24-char hex). |
| license_ids | array[string] | true | License ids from source org `get_licenses.licenses[].id`. |

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

- Path `orgId` is source org; body `org_id` is target org.
- Only licenses with `status=inactive` and no device association are eligible.
- Use `licenses[].id` only; never pass `license_key`.
