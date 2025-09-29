---
type: api-collection
title: Intrexx IntraDev — Portal API (Dev)
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/portal
  - env/dev
  - status/wip
  - spec/none
  - lang/de
  - collection/portal
  - exposure/internal-nonprod
  - api/collection
owner: Team Integration
base_url: https://<intradev-domain>
last_checked: YYYY-MM-DD
---



#  Contract

> [!danger] API OVERVIEW `¯\_(ツ)_/¯`
> **API_BASE** `=upper(this.api_base)`
> ---
> **QUERY** _tbd_ `¯\_(ツ)_/¯`  
> **RESPONSE** _tbd_ `¯\_(ツ)_/¯`

# Portal API (Dev) — Analyse

## Endpoints
- [[Intrexx_IntraDev_GetAuthenticationTokenTypes|Intrexx_intraDev_GetAuthenticationTokenTypes]]
- [[Intrexx_IntraDev_GetLoginDomains|Intrexx_intraDev_GetLoginDomains]]
- [[Intrexx_IntraDev_GetSessionInfo|Intrexx_intraDev_GetSessionInfo]]
- [[Intrexx_IntraDev_Login|Intrexx_intraDev_Login]]
- [[Intrexx_IntraDev_Logout|Intrexx_intraDev_Logout]]
- [[Intrexx_IntraDev_Upload|Intrexx_intraDev_Upload]]
- [[Intrexx_IntraDev_Download|Intrexx_intraDev_Download]]



## Status & Health
- [ ] 200 OK je Endpoint
- [ ] Parität zu Prod (Contracts identisch)
- [ ] Upload/Download auf Testdaten begrenzt, Max-Size/Quotas
- [ ] Fehlermodell konsistent
- [ ] CORS/Cookie-Domain/SameSite korrekt für Dev

## Auth & Tokens
- Session-/Token-Typ: _…_  
- Cookie-/Header-Namen: _…_  
- Test-Realms/Domains aus `getLoginDomains`: _…_

## Nutzung & Owner
- Consumer (Dev/QA): _…_  
- Deploy/Smoke-Tests: _…_

## Probleme / Risiken
- _…_

## Maßnahmen / Nächste Schritte
- _…_

## Relations
> [!tip]
> [[Intrexx_Intradev_Legacy]]
