---
type: system
title: "Intrexx Intranet Docu"
tags:
  - exposure/internal-live
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intranet
  - env/prod
  - status/active
  - spec/none          # openapi|postman|none → anpassen
  - auth/tbd           # oauth2|bearer|basic|apikey|none → anpassen
owner: "Team Integration"
service_owner: "…"
status: active
version_primary: v1
service_url: "https://intranet.example.tld/<pfad>"   # anpassen
openapi_url: ""               # URL oder leer
postman_collection: ""        # URL oder leer
last_reviewed: YYYY-MM-DD
sla: "99.9%/Monat"            # optional
slo: "P95 < 300ms"            # optional
---

# Intrexx Intranet API (Prod)

## Zusammenfassung
- **Zweck:** Kurzbeschreibung (Business-Capability, Hauptkonsumenten).
- **Scope/Boundaries:** In/Out of scope, sensible Daten, Mandanten.

## Architektur & Abhängigkeiten
- **Upstream:** [[…]] (Datenquellen)
- **Downstream/Consumer:** [[…]] (Verbraucher)
- **Datenflüsse:** Diagramm/Skizze verlinken.
- **Konfiguration/Secrets:** Speicherort verweisen (kein Klartext).

## Auth & Sicherheit
- **Auth:** oauth2/bearer/basic/apikey/none (Flows, Token-TTL).
- **Autorisierung:** Rollen/Scopes/Claims.
- **Transport:** TLS/mTLS, CORS.
- **PII/DSGVO:** Klassifikation, Aufbewahrung, Maskierung.

## Spezifikation & Kontrakte
- **OpenAPI/Postman:** siehe Frontmatter-Links.
- **Versionierung:** Pfad/Header, Deprecation-Policy, Sunset-Header.
- **Idempotenz:** Endpunkte + Schlüssel/Headers.

## Endpunkte (Inventar)
> bei Anlage/Änderung aktualisieren

| method | path | summary | version | auth | rate_limit | owner | deprecated | last_tested |
|-------:|------|---------|--------:|------|-----------:|-------|-----------:|-------------|
| GET | /api/v1/... | … | v1 | oauth2 | 60/min | Team X | no | YYYY-MM-DD |
| … | … | … | … | … | … | … | … | … |

## Fehler- & Antwortmodelle
- **Error format:** problem+json/json/xml (Beispiele, Codes).
- **Retry/Backoff:** Richtlinien, Idempotenzverhalten.

## Nicht-Funktionales
- **Performance-Ziele:** P95/P99, Payload-Größen.
- **Rate Limits & Quotas:** global/pro-Client.

## Monitoring & Observability
- **Dashboards:** Grafana/ELK-Links.
- **Logs/Traces/Metrics:** Standards, Korrelation (Trace-ID).
- **Alerting:** Regeln, On-Call-Kontakt.

## Tests & Qualität
- **Smoke/Contract-Tests:** Orte, CI-Trigger, Abdeckung.
- **Sicherheits-Checks:** Dependency/Container/DAST.

## Änderungen (Changelog)
- YYYY-MM-DD — Änderung — Impact — Ticket/Decision.

## Risiken
- Kurzliste + Mitigation/Owner.

## Verweise
- Tickets/Epics: [[…]]  — Runbooks: [[…]] — On-Call: [[…]]

## Relations
Links:: [[Intrexx_Intranet_Legacy]]
