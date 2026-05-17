Return the user profile.

### Response Body Example

```json
{
  "id": "5a46147afea16c00011156h8",
  "email": "admin@senao.com",
  "system_admin_email": null,
  "family_name": "Senao",
  "given_name": "cloud",
  "mobile": "0943123421",
  "company": "Senao",
  "country": "Taiwan",
  "time_zone": "America/Los_Angeles",
  "image": {
    "file_name": "senaocloud.jpg",
    "url": "https://<bucket-name>.s3.amazonaws.com/bae728c7-a7a3-4942-b9b5-3ca-b91126bb3d8f.image.jpg"
  },
  "language": "zh-TW",
  "recently_visited": {
    "org_id": "4e1cec404b0d5c86b9924bfb",
    "hierarchy_view_id": "66b7c33c52805aa6a8367f6d",
    "network_id": "e71bafb8dd75504a8ab9b87a"
  },
  "privacy_policy_time": 1514542202902,
  "created_time": 1514542202902,
  "modified_time": 1515047581234,
  "last_login_time": 1514542202902
}
```

### Response Body Schema

| Field               | Type    | Description                                      |
| ------------------- | ------- | ------------------------------------------------ |
| id                  | string  | User ID.                                         |
| email               | string  | User email.                                      |
| system_admin_email  | string \| null | System admin email, or null.              |
| family_name         | string  | Family name.                                     |
| given_name          | string  | Given name.                                      |
| mobile              | string  | Mobile number.                                   |
| company             | string  | Company name.                                    |
| country             | string  | Country.                                         |
| time_zone           | string  | IANA time zone (e.g. America/Los_Angeles).       |
| image               | object  | Profile image.                                   |
| language            | string  | Locale (e.g. zh-TW).                             |
| recently_visited    | object  |                                                  |
| privacy_policy_time | integer | UTC milliseconds when privacy policy was accepted. |
| created_time        | integer | UTC milliseconds when user was created.         |
| modified_time       | integer | UTC milliseconds when user was last modified.   |
| last_login_time     | integer | UTC milliseconds of last login.                  |


### image Schema (GET user/profile)

| Field      | Type   | Description        |
| ---------- | ------ | ------------------ |
| file_name  | string | Image file name.   |
| url        | string | Image URL.         |


### recently_visited Schema (GET user/profile)

| Field              | Type   | Description          |
| ------------------ | ------ | -------------------- |
| org_id             | string | Organization ID.     |
| hierarchy_view_id  | string | Hierarchy view ID.   |
| network_id         | string | Network ID.          |
