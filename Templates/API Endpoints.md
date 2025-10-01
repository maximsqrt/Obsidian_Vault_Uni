---
type: api-endpoint
auth: "[[Intranet_Key_Webkey]]"

title: <service_title>
tags:
  - project/<project>
  - system/<system>
  - app/<app>
  - env/<env>
  - exposure/<exposure>
  - status/<status>
owner: <owner>
guid_hash: ""
base_host: https://<host>:<port>
entity_paths:
  - /<entity_path_1>
  - /<entity_path_2>
  - /<entity_path_3>
method: GET
collection_ref: "[[]]"
last_checked: <YYYY-MM-DD>
---


#  Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=upper(this.auth)`
> ---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
> [!tip] BaseURL
> 
# Contract

> [!note] Übersicht
> 
> - **Method:** GET
>     
> - **Auth:** Benutzerkonto (Name/Passwort) erforderlich
>     
> - **Query-Params:** _tbd_
>     
> - **Response:** _tbd_
>     

```dataviewjs
const fm = dv.current().file.frontmatter;

// 1) Host ohne trailing Slash
const host = String(fm.base_host || "").replace(/\/+$/,"");

// 2) Servicename: override via 'service_name', sonst aus 'title' sluggen
const raw = String(fm.service_name || fm.title || dv.current().file.name || "");

// Slugify für DE (ASCII, stabil)
const service = fm.service_name ? raw : raw
  .replace(/ä/g,"ae").replace(/ö/g,"oe").replace(/ü/g,"ue")
  .replace(/Ä/g,"Ae").replace(/Ö/g,"Oe").replace(/Ü/g,"Ue")
  .replace(/ß/g,"ss")
  .normalize("NFKD").replace(/[\u0300-\u036f]/g,"")
  .toLowerCase().replace(/[^a-z0-9]+/g,"_").replace(/^_+|_+$/g,"");

// 3) Service-Root (mit .svc, falls gewünscht)
const base = `${host}/${service}.svc`;

// 4) Paths einsammeln (ein/mehrere)
let paths = [];
if (Array.isArray(fm.entity_paths)) paths = fm.entity_paths;
else if (Array.isArray(fm.paths)) paths = fm.paths;
else if (fm.entity_path) paths = [fm.entity_path];
else if (fm.path) paths = [fm.path];

// 5) Tabelle: Path | URL | Test-GET
const rows = (paths || []).map(p => {
  const seg = String(p || "");
  const url = base + (seg.startsWith("/") ? seg : "/" + seg);
  return [seg, `[${url}](${url})`, `[GET](${url})`];
});

// (Optional) Service-Root oberhalb ausgeben
dv.paragraph("**Service Root:** " + `[${base}](${base})`);

// Tabelle rendern
dv.table(["Path","URL","Test-GET"], rows);

```

> [!question] ## Relations

Parent:: 