---
type: system
title: "Intrexx IntraDev Docu"
tags:
  - exposure/internal-live
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intradev
  - env/dev            # env/stage, falls Staging separat
  - status/wip         # oder active, je nach Reife
  - spec/none
  - auth/tbd
owner: "Team Integration"
service_owner: "…"
status: wip
version_primary: v1
service_url: "https://intradev.example.tld/<pfad>"
openapi_url: ""
postman_collection: ""
last_reviewed: YYYY-MM-DD
---

# Intrexx IntraDev API (Dev/Stage)

## Zielsetzung
- Parität zu Prod (Funktions-, Daten-, Konfig-Parität).
- Sandbox-Besonderheiten, Testdatenstrategie.

## Unterschiede zu Prod
- **Features/Flags:** …
- **Datenmaskierung:** …
- **Auth/Test-Flows:** …
- **Dummy-Integrationen:** …

## Endpunkte (Inventar)
| method | path | summary | version | auth | rate_limit | owner | deprecated | last_tested |
|-------:|------|---------|--------:|------|-----------:|-------|-----------:|-------------|
| … | … | … | … | … | … | … | … | … |

## Spezifikation & Kontrakte
- OpenAPI/Postman (Dev-Stand), Kompatibilität zu Prod.
- Contract-Tests gegen Prod-Spez.

## Monitoring & Observability
- Dev-Dashboards/Logs, Alert-Tuning (reduziert).
- Testdaten-Richtlinien, Anonymisierung.

## Tests & Qualität
- **Smoke/Contract-Tests:** on-deploy.
- **Migrations/Seed:** Strategie, Rollback.

## Risiken & To-Dos bis Prod-Parität
- Kurzliste + Maßnahmen.

## Verweise
- Tickets/Epics: [[…]] — Testdaten: [[…]] — Pipelines: [[…]]

## Relations
Parent:: [[Intrexx Intranet API]]   <!-- falls als Parent genutzt -->
Links:: [[Inventory-Intrexx]], [[Intrexx-REST-3Wochen]]
Children:: <!-- gezielte Dev-Dossiers/Experimente verlinken -->
