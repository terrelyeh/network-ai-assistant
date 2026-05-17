# PATCH general-settings-plus Rules

When assembling or validating the request body for `patch_general_policy_plus`, the following rules must be followed. Rules are grouped by category; evaluate **every** rule in the rule-check table before finalizing the PATCH body.

---

## General Assembly

### R1. Array Field Mutations

- The PATCH API uses **full-replacement** semantics for array fields — the submitted array entirely replaces the existing one on the server.
- When the user requests adding, modifying, or removing items in an array field (e.g. `providers`, `white_list`, `block_list`):
  1. Start from the **complete existing array**. Use the dedicated candidates list if available (e.g. `wifi_calling_provider_candidates` for `providers`); otherwise read from the parent object in `general_policy_snapshot_candidates[0]`.
  2. Apply the user's intended mutation (append / update / remove) on that array.
  3. Send the **full resulting array** in the PATCH body.
- NEVER send only the new or changed items — this would silently delete all other existing items.

### R2. Field Exclusion — schedule_reboot

- The PATCH body must **never** include `ap_schedule_reboot` or `switch_schedule_reboot`.
- Regardless of whether the current API response or schema contains these fields, they MUST be explicitly removed when building the PATCH payload.

### R3. Country and compliance_record

- **When modifying country settings**: The PATCH body must include both:
  - `country` (the new value)
  - `compliance_record` (from country compliance data: `legal_name`, `datetime`)
- **When not modifying country**: The PATCH body MUST remove the `country` field.

---

## Feature-Gated Constraints

These rules protect sub-fields from modification when their parent feature is disabled. If the user insists, guide them to enable the parent feature first.

### R4. Custom NTP Server

- Modification of `port` or `host` is allowed **only when** `custom_ntp_server` `is_enable` is `true`.
- If `is_enable` is `false`, do not modify `port` or `host`.

### R5. WiFi Calling

- When `ap_wifi_calling` `is_enable` is `false`, the following fields MUST NOT be modified:
  - `qos_priority`
  - `providers`

---

## Domain-Specific Rules

### R6. LAN Port Settings

#### LAN Port Number Mapping


| LAN Label | `port` field value |
| --------- | ------------------ |
| LAN 2     | `1`                |
| LAN 3     | `2`                |


#### vlan_mode Reference


| vlan_mode value | Meaning                                                                 |
| --------------- | ----------------------------------------------------------------------- |
| `"trunk"`       | Tagged device only — port carries tagged VLAN traffic.                  |
| `"access"`      | Untagged device only — port carries untagged traffic for a single VLAN. |
| `"disable"`     | Bypassed all — VLAN is disabled on this port.                           |


#### Rules

When the PATCH body includes LAN port changes, apply the following rules in order:

- **Target field**: Only modify `lan_ports_by_model`. Do NOT include or modify the top-level `lan_ports` field.
- **Model matching**: Find the entry in `lan_ports_by_model` whose `model_name` matches the target model, then update only the relevant items in its `ports` array.
- **Disabled port**: When a port's `is_enable` is `false`, the following fields MUST NOT be modified for that port:
  - `vlan_mode`
  - `vlan_id`
  - `ssid_profile_id`
  - `is_casting_on_lan_enable`
- **SSID assignment**: Use the SSID name lookup table from state discovery to resolve the user-provided SSID name to its `ssid_profile_id`. To remove the SSID assignment from a port, set `ssid_profile_id` to `""`.
- **SSID profile active**: When `ssid_profile_id` is a non-empty string, the following fields MUST NOT be modified for that port:
  - `vlan_mode`
  - `vlan_id`
- **VLAN disabled**: When `vlan_mode` is `"disable"`, `vlan_id` MUST NOT be modified for that port.
