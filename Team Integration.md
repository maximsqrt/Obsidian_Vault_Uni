---
owner_team: "integration"
owner_display: "@team-integration"
owner_oncall: "ops/integration-oncall"
owner_contact_primary: "slack://#team-integration"   # oder mailto:
owner_contact_backup: "slack://#platform-oncall"
owner_repo: ["group/project-a","group/project-b"]     # GitLab Pfade
owner_services: ["publications","users"]              # betroffene APIs/Services
support_hours: "24/7"
slo_availability: "99.9%"
slo_latency_p50_ms: 120
slo_latency_p95_ms: 350
runbook_urls: ["https://…/runbooks/publications","https://…/runbooks/users"]
cmdb_ci: "svc-integration"
data_owner: "integration"
security_contact: "sec@company.tld"
pii: false
---

> [!tip] Schnellkontakt
> **Owner:** {{owner_display}}  
> **On-Call:** {{owner_oncall}}  
> **Chat:** {{owner_contact_primary}} · **Fallback:** {{owner_contact_backup}}

> [!info] Zuständigkeit (Scope)
> **Services:** {{owner_services}}  
> **Code:** {{owner_repo}}  
> **CI/CD:** Ownership für Build, Deploy, Rollback der oben genannten Repos.

> [!warning] Betriebsziele (SLO)
> **Verfügbarkeit:** {{slo_availability}} · **Latenz:** p50 ≤ {{slo_latency_p50_ms}} ms, p95 ≤ {{slo_latency_p95_ms}} ms  
> **Supportzeiten:** {{support_hours}}  
> **PII:** {{pii}} · **Security-Kontakt:** {{security_contact}}

> [!example] Runbooks (Top-3)
> 1. **Incident-Bootstrap:** wie Log/Trace/Metric anwerfen → {{runbook_urls[0]}}
> 2. **Rollback/Feature-Toggle:** Pfad & Checks → {{runbook_urls[1]}}
> 3. **Token/Auth-Störungen:** Ablauf & Eskalation → Link ergänzen

> [!abstract] Eskalation & Governance
> **Stufe 1:** {{owner_display}} / {{owner_contact_primary}}  
> **Stufe 2:** {{owner_oncall}} (Telefon/Pager)  
> **Stufe 3:** Incident-Commander (Platform)  
> **Change-Policy:** SemVer, Breaking only mit `v{n+1}`, Deprecation ≥ 90 Tage  
> **Data Owner:** {{data_owner}} · **CMDB/CI:** {{cmdb_ci}}

> [!note] Artefakte
> - **Dashboards:** Link zu prod/stg Observability
> - **Alarme:** Link zu Alert-Policies
> - **Postmortems:** Ordnerlink
> - **Service-Karte:** Architektur/Dependency-Map

