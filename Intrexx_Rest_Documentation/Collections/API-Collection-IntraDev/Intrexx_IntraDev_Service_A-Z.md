---
type: api-collection
title: "Intrexx IntraDev API — Service A–Z"
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intradev
  - env/dev
  - exposure/internal-nonprod
  - status/wip
  - spec/none
  - lang/de
  - collection/service-a-z
owner: "Team Integration"
app_id: "99AF5C20962E81CA332D0C3FC64841FE96BE7173"
base_url: "[[BaseURL_intraDev]]"
api_base: "[[BaseURL_intraDev]]/api/app/99AF5C20962E81CA332D0C3FC64841FE96BE7173"
endpoints_count: 6
last_checked: YYYY-MM-DD
---

# Service A–Z — Analyse

## Endpoints
- `<GET>` <[[BaseURL_intraDev]]/api/app/99AF5C20962E81CA332D0C3FC64841FE96BE7173/beitraege>
- `<GET>` <[[BaseURL_intraDev]]/api/app/99AF5C20962E81CA332D0C3FC64841FE96BE7173/beitrag{strid}>
- `<GET>` <[[BaseURL_intraDev]]/api/app/99AF5C20962E81CA332D0C3FC64841FE96BE7173/formular/{strid}>
- `<GET>` <[[BaseURL_intraDev]]/api/app/99AF5C20962E81CA332D0C3FC64841FE96BE7173/formulare>
- `<GET>` <[[BaseURL_intraDev]]/api/app/99AF5C20962E81CA332D0C3FC64841FE96BE7173/gformulare>
- `<GET>` <[[BaseURL_intraDev]]/api/app/99AF5C20962E81CA332D0C3FC64841FE96BE7173/gbeitraege>

## Status & Health
- [ ] 200 OK je Endpoint
- [ ] Auth / Rollen (Session/Cookie/Token) geklärt
- [ ] Pagination/Filter (falls Listen)
- [ ] Fehlermodell konsistent (z. B. problem+json)
- [ ] Rate Limits/Quotas dokumentiert

## Auth & Keys
- Typ: _(oauth2 | bearer | basic | apikey | none)_  
- Übergabe: _(Header `Authorization`, Cookie, Query …)_  
- Scopes/Rollen: _…_

## Nutzung & Owner
- Consumer: _…_  
- Nutzung: _aktiv / selten / unklar_

## Probleme / Risiken
- _…_

## Maßnahmen / Nächste Schritte
- _…_

## Relations
Parents:: [[Intrexx-REST-Discovery]], [[Inventory-Intrexx]]  
Links:: [[Intrexx-REST-3Wochen]], [[Dashboard_API_BASE]], [[Intrexx-Intradev-Docu]]
