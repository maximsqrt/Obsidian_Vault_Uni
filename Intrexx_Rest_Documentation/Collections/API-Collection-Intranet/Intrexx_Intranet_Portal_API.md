---
type: api-collection
title: Intrexx Intranet — Portal API (Prod)
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/portal
  - env/prod
  - exposure/internal-live
  - status/wip
  - spec/none
  - lang/de
  - collection/portal
  - api/collection
owner: Team Integration
base_url: https://<intranet-domain>
last_checked: YYYY-MM-DD
---



#  Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=upper(this.auth)`
> ---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
# Portal API (Prod) — Analyse

## Endpoints
- `POST` <https://<intranet-domain>/service/login/getAuthenticationTokenTypes>
- `GET` <https://<intranet-domain>/service/login/getLoginDomains>
- `POST` <https://<intranet-domain>/service/login/getSessionInfo>
- `POST` <https://<intranet-domain>/service/login/login>
- `GET` <https://<intranet-domain>/service/login/logout>
- `POST` <https://<intranet-domain>/api/app/upload>
- `GET`  <https://<intranet-domain>/api/app/download>

## Status & Health
- [ ] 200 OK je Endpoint
- [ ] Auth-Endpunkte Reihenfolge/Contract klar (Inputs/Outputs)
- [ ] Upload: `multipart/form-data` angenommen, Max-Size, Response
- [ ] Download: Auth-Zwang, Content-Disposition, Caching
- [ ] Fehlermodell konsistent (z. B. problem+json)
- [ ] Rate Limits/Throttling dokumentiert

## Auth & Tokens
- Session-Typ: _(Cookie/Token)_  
- Cookie-/Header-Namen: _…_  
- Geltungsbereich/Scopes: _…_  
- CSRF-/Anti-Replay-Mechanismen (falls): _…_

## Nutzung & Owner
- Consumer: _…_  
- Nutzung (aktiv/selten/unklar): _…_

## Probleme / Risiken
- _…_

## Maßnahmen / Nächste Schritte
- _…_

## Relations
> [!tip]
> [[Intrexx_Intranet_Legacy]]
