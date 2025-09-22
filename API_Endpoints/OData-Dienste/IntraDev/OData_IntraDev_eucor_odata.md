---
type: api-endpoint
title: eucor_odata (IntraDev)
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intradev
  - env/dev
  - exposure/internal-nonprod
  - status/wip
  - spec/odata-v4
  - lang/de
  - endpoint/eucor_odata
  - method/get
  - status/active
owner: Team Integration
guid_hash: ""
base_url: "[[BaseURL_OData_IntraDev]]"
path_prefix: /eucor_view$4
method: GET
collection_ref: "[[]]"
last_checked: 2025-09-02
---



# `eucor_odata` — Contract

> [!note] Übersicht
> - **Method:** GET
> - **Auth:** Benutzerkonto (Name/Passwort) erforderlich
> - **Query-Params:** _tbd_
> - **Response:** _tbd_


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

Parent:: [[OData_Hinweise_und_Erläuterungen]]