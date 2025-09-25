---
type: api-endpoint
auth: x-api-key

title: TEST — alle Tags (IntraDev)
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intradev
  - env/dev
  - exposure/internal-nonprod
  - spec/odata-v4
  - spec/none
  - lang/de
  - collection/test-collection
  - endpoint/test-endpoint
  - method/get
  # ---- alle Status-Varianten für Badge-Tests ----
  - status/active
  - status/wip
  - status/deprecated
  - status/http-4xx
  - status/http-5xx
owner: Team Integration
guid_hash: 1CB22DE7420AEC12CCE7B27740A4845F7DB7F16A
base_url: "[[BaseURL_intraDev]]"
path_prefix: /api/app
path_entities:
  - "/themen"
method: GET
collection_ref: "[[Intrexx_IntraDev_Veranstaltungen_und_Termine]]"
last_checked: 2025-08-27
---

# Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=upper(this.auth)`
> ---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
