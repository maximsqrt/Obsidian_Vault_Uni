---
type: note
title: OData_Hinweise_und_Erläuterungen
tags:
  - spec/odata-v4
  - guideline
  - lang/de
  - collection/datendrehscheibe
  - api/collection
owner: Team Integration
last_reviewed: 2025-09-03
---



#  Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=upper(this.auth)`
> ---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
last_reviewed: 2025-09-03
---


# OData — Hinweise & Erläuterungen

> [!note] TL;DR (für API-Notes als _Parent_)
> 
> - **Schnittstelle:** OData v4 (HTTP/REST), **Service Root** i. d. R. mit **`.svc`**
>     
> - **Auth:** Benutzerkonto (Name/Passwort) erforderlich (Basic über TLS oder gültige Session)
>     
> - **Service-Root-Antwort:** listet **EntitySets**, z. B.  
>     `{"d":{"EntitySets":["eucor_view"]}}`
>     
> - **Abruf:** Aufruf von `/<entity-set>` (z. B. `/eucor_view`) liefert **alle Datensätze**, wenn **kein** Filter/Paging aktiv ist
>     
> - **Query-Optionen:** `$filter`, `$select`, `$orderby`, `$top/$skip`, `$count`, optional `$format`, Header `Accept: application/json`
>     

## Service Root & `.svc`

- Die Basis-URL eines OData-Dienstes ist der **Service Root** (häufig mit Endung **`.svc`** bei Intrexx/WCF-Hosts).
    
- `GET <service-root>` liefert ein **Servicedokument** mit den verfügbaren **EntitySets** (Collections).
    

**Beispiel (vereinfacht):**

```json
{
  "d": {
    "EntitySets": ["eucor_view"]
  }
}
```

## EntitySet-Aufrufe & Rückgabemenge

- `GET <service-root>/<entity-set>` ruft die **Collection** des EntitySets ab.
    
- Ohne `$filter`, `$top/$skip` **und** ohne serverseitiges Paging kommt **die komplette Ergebnismenge** zurück.
    
- Begrenzen über Client: `$top=N&$skip=M`.
    
- Serverseitig begrenzen: **server-driven paging** (MaxPageSize) im Service.
    

## Authentifizierung

- Zugriff setzt **Benutzerkonto** (Username/Passwort) voraus.
    
- Üblich: **HTTP Basic** über TLS oder ein vorhandener **Intrexx-Session-Cookie**.
    
- Das Konto benötigt **Leserechte** auf die zugrunde liegende Quelle/App.
    

## OData-Query-Optionen (Kurzreferenz)

- `$filter=Expr` – serverseitige Filterung (z. B. `Status eq 'active'`)
    
- `$select=Feld1,Feld2` – Projektion/Spaltenauswahl
    
- `$orderby=Feld [asc|desc]` – Sortierung
    
- `$top=N` / `$skip=M` – Paging
    
- `$count=true` – Gesamtanzahl mitschicken
    
- `$format=json` – Ausgabeformat (optional; mit `Accept: application/json` meist entbehrlich)
    

## URL-Zusammenbau in Obsidian (Dataview)

Empfohlene Frontmatter-Felder in der API-Note:

```yaml
base_url: 'https://<host>:<port>/<service>.svc'
path_prefix: 'eucor_view'          # oder mit führendem Slash: '/eucor_view'$4
```

**Inline-Dataview** für klickbare URL im Body (Callout etc.):

- Falls `path` **ohne** führenden Slash:
    

```
<`= this.base_url + "/" + this.path`>
```

- Falls `path` **mit** führendem Slash:
    

```
<`= this.base_url + this.path`>
```

**Beispiel-Callout in der API-Datei:**

```md
> [!note] Übersicht
> - **Method:** GET
> - **URL:** <`= this.base_url + "/" + this.path`>
> - **Auth:** Benutzerkonto (Name/Passwort) erforderlich
> - **Query-Params:** _tbd_
> - **Response:** _tbd_
```

## Beispiele

**Service-Root (EntitySets entdecken):**

```
GET <service-root>
Accept: application/json
```

**Alle Datensätze eines EntitySets (ungefiltert):**

```
GET <service-root>/eucor_view
Accept: application/json
```

**Gefiltert & paginiert:**

```
GET <service-root>/eucor_view?$select=Id,Name,Status&$filter=Status eq 'active'&$orderby=Id asc&$top=100&$skip=0
Accept: application/json
```

---








#  Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=upper(this.auth)`
> ---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
> [!danger] Achtung
> #### OData_IntraDev
> ```dataview
list
from ""
where file.ext = "md" and contains(file.name, "OData_IntraDev")
sort file.name asc
> ```
>
> #### OData_Intranet
> ```dataview
list
from ""
where file.ext = "md" and contains(file.name, "OData_Intranet")
sort file.name asc
> ```





