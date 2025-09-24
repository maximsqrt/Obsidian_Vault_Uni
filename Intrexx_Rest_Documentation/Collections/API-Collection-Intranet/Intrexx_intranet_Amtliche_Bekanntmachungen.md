---
type: api-collection
title: "Intrexx Intranet API — Amtliche Bekanntmachungen"
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intranet
  - env/prod
  - exposure/internal-live
  - status/wip
  - spec/none
  - lang/de
  - collection/amtliche-bekanntmachungen
owner: "Team Integration"
guid_hash: "6731A8BF6579F6E079F2913C8FA92ADC4EACA7C5"
api_base: "[[BaseURL_Intranet]]/api/app/6731A8BF6579F6E079F2913C8FA92ADC4EACA7C5"
endpoints_count: 1
last_checked: YYYY-MM-DD
path_prefix: /api/app
---



#  Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=upper(this.auth)`
> ---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
# Amtliche Bekanntmachungen — Analyse

## Endpoints
- `GET` <[[BaseURL_Intranet]]/api/app/6731A8BF6579F6E079F2913C8FA92ADC4EACA7C5/amtlbek>

## Status & Health
- [ ] Grundfunktion 200 OK
- [ ] Auth korrekt (s. unten)
- [ ] Pagination (falls Liste)
- [ ] Fehlermodell konsistent (problem+json o.ä.)
- [ ] Rate Limits dokumentiert

## Auth & Keys
- Typ: _(oauth2|bearer|basic|apikey|none)_  
- Key/Token-Ort: _(Header `Authorization`, Query `apikey`, Cookie …)_  
- Parameter/Scope: _…_

## Nutzung & Owner
- Consumer: _Teams/Apps_  
- Nutzung (aktiv/selten/unklar): _…_

## Probleme / Risiken
- _…_

## Maßnahmen / Nächste Schritte
- _…_

## Relations
> [!tip]
> [[Intrexx_Intranet_Legacy]]
