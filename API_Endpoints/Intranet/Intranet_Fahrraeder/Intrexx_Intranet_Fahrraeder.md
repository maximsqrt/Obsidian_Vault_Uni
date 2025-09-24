---
type: api-endpoint
title: Fahrräder — fahrraeder (Intranet)
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intranet
  - env/prod
  - exposure/internal-live
  - status/wip
  - spec/none
  - lang/de
  - collection/fahrraeder
  - endpoint/fahrraeder
  - method/get
  - status/active
owner: Team Integration
guid_hash: 43FCB1E50030712AA3E5E8C30402319D1ED66995
base_url: "[[BaseURL_Intranet]]"
path_prefix: /api/app
path_entities: "/fahrraeder"
method: GET
collection_ref: "[[Intrexx_Intranet_Fahrradverwaltung]]"
last_checked: YYYY-MM-DD
---


# `fahrraeder` — Contract
- **Method:** GET  
- **URL:** <[[BaseURL_Intranet]]/api/app/43FCB1E50030712AA3E5E8C30402319D1ED66995/fahrraeder>  
- **Auth:** _tbd_  
- **Query-Params:** _tbd_  
- **Response:** _tbd_

## Status & Health
- [ ] 200 OK
- [ ] Pagination/Filter
- [ ] Fehlermodell

## Relations
Parent:: [[Intrexx_Intranet_Fahrradverwaltung]]


```dataviewjs
// Read frontmatter
const fm = dv.current().file.frontmatter;

// Base URL without trailing slash
const base = String(fm.base_url || "").replace(/\/+$/,"");

// Collect paths (supports multiple field names)
let paths = [];
if (Array.isArray(fm.entity_paths)) paths = fm.entity_paths;
else if (Array.isArray(fm.paths)) paths = fm.paths;
else if (fm.entity_path) paths = [fm.entity_path];
else if (fm.path) paths = [fm.path];

// Build rows: Path | URL | Test-GET
const rows = paths.map(p => {
  const seg = String(p || "");
  const url = base + (seg.startsWith("/") ? seg : "/" + seg);
  return [seg, `[${url}](${url})`, `[GET](${url})`];
});

// Render table (headers)
dv.table(["Path", "URL", "Test-GET"], rows);
```

> [!question] ## Relations
> Parent:: [[OData_Hinweise_und_Erläuterungen]]