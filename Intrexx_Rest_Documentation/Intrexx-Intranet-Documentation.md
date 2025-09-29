---
type: system
title: Intrexx Intranet Docu
tags:
  - exposure/internal-live
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intranet
  - env/prod
  - status/active
  - spec/none
  - auth/tbd
owner: Team Integration
service_owner: "\n"
status: active
version_primary: v1
service_url: https://intranet.example.tld/<pfad>
openapi_url: ""
postman_collection: ""
last_reviewed: YYYY-MM-DD
sla: 99.9%/Monat
slo: P95 < 300ms
path_prefix: /api/app
---



#  Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=upper(this.auth)`
> ---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
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



## Relations
Links:: [[Intrexx_Intranet_Legacy]]
