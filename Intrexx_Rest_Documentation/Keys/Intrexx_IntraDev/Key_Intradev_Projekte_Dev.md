---
type: key
title: "Key IntraDev — Projekte (Dev)"
tags:
  - project/intrexx-rest-discovery
  - auth/key
  - key/status/review
  - system/intrexx
  - app/intradev
  - env/dev
  - exposure/internal-nonprod
owner: "Team Integration"
key_id: "Projekte"
key_type: "tbd"              # apikey | bearer-static | oauth2-client | mtls-cert
auth_flow: "tbd"             # header-bearer | cookie-session | query-apikey | …
secret_ref: "vault://intraDev/dev/projekte/Projekte"
endpoints_count: 0           # aktualisieren, sobald bekannt
usage_refs:
  - [[Intrexx-IntraDev-API-Tests]]           # enthält /projekte
endpoint_refs: []
last_checked: YYYY-MM-DD
---

## Zweck & Umfang
Zugriff für „Projekte“-Funktionalität in IntraDev.

## Integration
- **Key-Typ:** {{key_type}} — **Auth-Flow:** {{auth_flow}}
- **Übergabe:** Header/Query/Cookie (genaue Namen festhalten)
- **Secret:** {{secret_ref}}

## Status & ToDos
- Tag: `key/status/review`
- [ ] Key-Typ/Flow verifizieren
- [ ] Endpunkte & Consumer zuordnen (Tests-Collection)
- [ ] Rotation/Expiry dokumentieren
