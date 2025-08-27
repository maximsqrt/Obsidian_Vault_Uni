---
type: key
title: "Key Allgemein — Rahmenverträge (Intranet Prod)"
tags:
  - project/intrexx-rest-discovery
  - auth/key
  - key/status/review
  - system/intrexx
  - app/intranet
  - env/prod
  - exposure/internal-live
  - role/allgemein
owner: "Team Integration"
key_id: "Rahmenverträge"
key_type: "tbd"
auth_flow: "tbd"
secret_ref: "vault://intrexx/intranet/prod/vergebene-auftraege/Rahmenvertraege"
endpoints_count: 4
usage_refs:
  - [[Intrexx-Intranet-API-Vergebene-Auftraege]]
endpoint_refs:
  - /api/app/E14074D19E1FB8644E124BC295F886FDED6CBE51/rahmenvertraege
  - /api/app/E14074D19E1FB8644E124BC295F886FDED6CBE51/vob
  - /api/app/E14074D19E1FB8644E124BC295F886FDED6CBE51/binnenmarkt
  - /api/app/E14074D19E1FB8644E124BC295F886FDED6CBE51/vergeben
last_checked: YYYY-MM-DD
---

## Zweck & Umfang
Allgemeiner Key für Vergaben/Rahmenverträge (4 Endpunkte).

## Integration & Status
(siehe Template oben) – Tag: `key/status/review`
