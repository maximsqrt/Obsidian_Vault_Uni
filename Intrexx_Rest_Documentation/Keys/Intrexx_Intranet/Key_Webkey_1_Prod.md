---
type: key
title: "Key Web — WEBKEY #1 (Intranet Prod)"
tags:
  - project/intrexx-rest-discovery
  - auth/key
  - key/status/review
  - system/intrexx
  - app/intranet
  - env/prod
  - exposure/internal-live
  - role/web
owner: "Team Integration"
key_id: "WEBKEY"
key_type: "tbd"            # apikey | bearer-static | oauth2-client | mtls-cert
auth_flow: "tbd"           # header-bearer | cookie-session | query-apikey | …
secret_ref: "vault://intrexx/intranet/prod/web/WEBKEY"
endpoints_count: 34
usage_refs:
  - [[Intrexx_Intranet_Veranstaltungen_und_Termine-und-Termine]]
  - [[Intrexx-Intranet-API-Studiengaenge]]
  - [[Intrexx_Intranet_Stellenausschreibungenausschreibungen]]
  - [[Intrexx-Intranet-API-Service-A-Z]]            # anlegen, falls noch nicht vorhanden
  - [[Intrexx-Intranet-API-Fundsachen]]
  - [[Intrexx-Intranet-API-Vergebene-Auftraege]]
endpoint_refs: []          # optional: einzelne Pfade ergänzen
last_checked: YYYY-MM-DD
---

## Zweck & Umfang
Web-weit genutzter Key für X/Y. Gilt für ~34 Endpunkte (siehe Collections).

## Integration
- **Key-Typ:** {{key_type}} — **Auth-Flow:** {{auth_flow}}
- **Übergabe:** Header/Query/Cookie (genau benennen)
- **Secret:** {{secret_ref}}

## Verknüpfte Schnittstellen
Siehe **Usage refs** (Sammlungen) und ggf. **endpoint_refs** (präzise Pfade).

## Status & ToDos
- Tag: `key/status/review` → **prüfen & vervollständigen**
- [ ] Key-Typ/Flow verifizieren
- [ ] Consumer/Owner vervollständigen
- [ ] Rotation/Expiry setzen
- [ ] Rate Limits dokumentieren
