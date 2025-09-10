---
type: plan
title: "Intrexx REST – 3 Wochen"
tags: [Projekt/Intrexx-REST-Discovery, Area/Integration]
---

# Plan – Intrexx REST – 3 Wochen (2025-08-25–2025-09-14)
Bezug: [[Intrexx-Intradev-Documentation]] · Inventar: [[Inventory-Intrexx]]

## Woche 1 — Discovery (2025-08-25–2025-08-31)

# Checkup – Überblick
- [x] Obsidian Intrexx / intradev API-Sachen eingefügt
- [ ] Logdateien: SQL-Preset für Analyse bauen (API-Nutzung erkennen: **ob** und **wie**)
- [ ] API-Keys: Inventar & Aufräumen (ungenutzte Keys stilllegen; Zielbild klären: 1 Key vs. mehrere)
- [ ] Intranet vs. Dev: unterschiedliche APIs/Daten – Entscheidungsvorlage „soll das so?“
- [ ] Postman: Swagger/OpenAPI-konforme Template-Collection für FastAPI-Checks
- [ ] Fremd-APIs aus Intrexx katalogisieren (so weit wie möglich)


### Kritisch
- [x] Möglich 
- [x] Zugänge, Keys und Token inventarisieren (alle Systeme, Vault, Umgebungen)  start: 2025-08-25 scheduled: 2025-08-26 due: 2025-08-29 priority: high #Projekt/Intrexx-REST-Discovery ✅ 2025-09-01
- [x] Basis-URLs und API-Hosts ermitteln (DNS, Reverse Proxy, App-Konfiguration)  start: 2025-08-25 scheduled: 2025-08-27 due: 2025-08-29 priority: high #Projekt/Intrexx-REST-Discovery ✅ 2025-09-01
- [x] Initiales API-Inventar anlegen (Dossiers je Endpoint beginnen)  start: 2025-08-26 scheduled: 2025-08-27 due: 2025-08-29 priority: high #Projekt/Intrexx-REST-Discovery ✅ 2025-09-01
- [ ] Logquellen und Metriken identifizieren (Access-/App-Logs, Proxy, APM)  start: 2025-08-26 scheduled: 2025-08-28 due: 2025-08-29 priority: high  #Projekt/Intrexx-REST-Discovery
- [ ] Test-Harness bereitstellen (curl/httpie, Postman-Collection, Python httpx)  start: 2025-08-27 scheduled: 2025-08-28 due: 2025-08-29 priority: high  #Projekt/Intrexx-REST-Discovery

### Wichtig
- [ ] Authentifizierungsflüsse verifizieren (Bearer, API-Key, Basic; Token-Refresh)  start: 2025-08-27 due: 2025-08-29 priority: medium  #Projekt/Intrexx-REST-Discovery
- [ ] Well-known-Pfade prüfen (/openapi.json, /swagger, /api-docs, /v3/api-docs)  start: 2025-08-27 due: 2025-08-29 priority: medium  #Projekt/Intrexx-REST-Discovery
- [ ] Klassifikationsschema fixieren (status, used, risk, owner)  start: 2025-08-28 due: 2025-08-29 priority: medium  #Projekt/Intrexx-REST-Discovery

### Nice-to-have
- [ ] Erste Response-Samples sichern (Evidence) und minimale Feldlisten je Ressource  start: 2025-08-28 due: 2025-08-30 priority: low  #Projekt/Intrexx-REST-Discovery
- [ ] Grobe Data-Flow-Skizze (Quelle → Service → Endpoint)  start: 2025-08-28 due: 2025-08-31 priority: low  #Projekt/Intrexx-REST-Discovery

---

## Woche 2 — Verifikation (2025-09-01–2025-09-07)

### Kritisch
- [ ] Je Endpoint: Happy Path (2xx) und Fehlerpfade (4xx/5xx) testen; Dossier aktualisieren  start: 2025-09-01 scheduled: 2025-09-02 due: 2025-09-05 priority: high  #Projekt/Intrexx-REST-Discovery
- [ ] Pagination, Filter und Sortierung prüfen (Parameter, Limits, Defaults)  start: 2025-09-02 scheduled: 2025-09-03 due: 2025-09-05 priority: high  #Projekt/Intrexx-REST-Discovery
- [ ] Idempotenz und Nebenwirkungen bewerten (PUT/PATCH/DELETE)  start: 2025-09-02 scheduled: 2025-09-04 due: 2025-09-05 priority: high  #Projekt/Intrexx-REST-Discovery
- [ ] Broken/Blocked markieren; Grund und benötigte Owner/Keys dokumentieren  start: 2025-09-03 due: 2025-09-05 priority: high  #Projekt/Intrexx-REST-Discovery

### Wichtig
- [ ] Halbautomatische Probe-Skripte (Python httpx) für GET/POST/OPTIONS/HEAD  start: 2025-09-01 due: 2025-09-04 priority: medium  #Projekt/Intrexx-REST-Discovery
- [ ] Schema grob extrahieren (Felder, Typen, Pflicht, Beispiele)  start: 2025-09-03 due: 2025-09-05 priority: medium  #Projekt/Intrexx-REST-Discovery
- [ ] Rate Limits/Throttling empirisch messen (Retry-Header, Backoff)  start: 2025-09-03 due: 2025-09-05 priority: medium  #Projekt/Intrexx-REST-Discovery

### Nice-to-have
- [ ] Baseline-Latenzen je Ressource (P50/P95)  start: 2025-09-03 due: 2025-09-06 priority: low  #Projekt/Intrexx-REST-Discovery
- [ ] Negative Tests (ungültige Payloads, fehlende Auth, Grenzwerte)  start: 2025-09-04 due: 2025-09-07 priority: low  #Projekt/Intrexx-REST-Discovery
- [ ] OpenAPI-Stubs pro Ressource (minimal) generieren  start: 2025-09-04 due: 2025-09-07 priority: low  #Projekt/Intrexx-REST-Discovery

---

## Woche 3 — Nutzung und Entscheidungen (2025-09-08–2025-09-14)

### Kritisch
- [ ] Nutzung analysieren (Logs 90 Tage: Top-Endpoints, 0-Hits, Trends)  start: 2025-09-08 scheduled: 2025-09-09 due: 2025-09-12 priority: high  #Projekt/Intrexx-REST-Discovery
- [ ] Liste „Unused/Broken/Deprecated“-Kandidaten finalisieren; Impact bewerten  start: 2025-09-09 due: 2025-09-12 priority: high  #Projekt/Intrexx-REST-Discovery
- [ ] Owner-Abgleich und Entscheidungen einholen (weiterführen, fixen, deprecaten)  start: 2025-09-10 due: 2025-09-12 priority: high  #Projekt/Intrexx-REST-Discovery
- [ ] Inventory und Gaps konsolidieren (Inventory-Intrexx; Dossiers vollständig)  start: 2025-09-10 due: 2025-09-12 priority: high  #Projekt/Intrexx-REST-Discovery

### Wichtig
- [ ] OpenAPI-Skeletons für genutzte Endpoints vervollständigen  start: 2025-09-10 due: 2025-09-12 priority: medium  #Projekt/Intrexx-REST-Discovery
- [ ] ADRs zu Auth-Standards und Paging-Konventionen erstellen (kurz)  start: 2025-09-10 due: 2025-09-12 priority: medium  #Projekt/Intrexx-REST-Discovery

### Nice-to-have
- [ ] Postman-Testsuite und Smoke-Checks (CI-fähig)  start: 2025-09-10 due: 2025-09-13 priority: low  #Projekt/Intrexx-REST-Discovery
- [ ] Kleine Übersichts-Dashboards (Nutzung, Latenzen)  start: 2025-09-11 due: 2025-09-14 priority: low  #Projekt/Intrexx-REST-Discovery

---

## Relations
Parents:: [[Intrexx-Intradev-Documentation]]
Links:: [[Inventory-Intrexx]], [[Dashboard_API_BASE]]
