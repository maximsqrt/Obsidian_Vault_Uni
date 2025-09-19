---
type: api-endpoint
title: user
guid_hash: E8F7687AE12876495F0A5B3C43321B695AA48561
path_prefix: /api/app
owner: Team Integration
base_url: "[[BaseURL_IntraDev]]"
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - env/dev
  - exposure/internal-nonprod
  - status/wip
  - spec/odata-v4
  - lang/de
  - method/get
  - app/intradev
  - status/active
path_entities:
  - /user
method: GET
last_checked: 2025-09-02
collection_ref: "[[Intrexx_Rest_Documentation/Collections/API-Collection-IntraDev/Intrexx_IntraDev_Datendrehscheibe|Intrexx_IntraDev_Datendrehscheibe]]"
---


#  Contract

> [!tip] Übersicht
> 
> - **Method:** GET
>     
> - **URL:**
>     
> 
> ```dataviewjs
> const fm = dv.current().file.frontmatter;
> const host = String(fm.base_host || "").replace(/\/+$/,"");        // "[[BaseURL_IntraDev]]" bleibt Link-Text
> const up = fm.url_parts || {};
> const prefix = String(up.path_prefix || "/api/app").replace(/\/+$/,""); // Fallback: /api/app
> const guid = String(up.app_guid || fm.guid_hash || "").trim();
> const service = String(fm.title || "").trim();                      // "amtlbek"
> 
> const url = [host, prefix.replace(/^\//,""), guid, service]
>   .filter(Boolean).join("/");
> 
> dv.paragraph(`[${url}](${url})`);
> ```
> 
> - **Auth:** Benutzerkonto (Name/Passwort) erforderlich
>     
> - **Query-Params:** _tbd_
>     
> - **Response:** _tbd_
>     




```dataviewjs
const fm = dv.current().file.frontmatter;

// Host ohne trailing Slash
const host = String(fm.base_host || "").replace(/\/+$/,"");

// Servicename: override via 'service_name', sonst aus 'title' sluggen
const raw = String(fm.service_name || fm.title || dv.current().file.name || "");
const service = fm.service_name ? raw : raw
  .replace(/ä/g,"ae").replace(/ö/g,"oe").replace(/ü/g,"ue")
  .replace(/Ä/g,"Ae").replace(/Ö/g,"Oe").replace(/Ü/g,"Ue")
  .replace(/ß/g,"ss")
  .normalize("NFKD").replace(/[\u0300-\u036f]/g,"")
  .toLowerCase().replace(/[^a-z0-9]+/g,"_").replace(/^_+|_+$/g,"");

// Nur eine URL (BaseURL/amtlbek) in der Tabelle ausgeben
const url = `${host}/${service}`;
dv.table(["URL"], [[`[${url}]`]]);

```

# Parent 
> [!note]
> [[Intrexx_Rest_Documentation/Collections/API-Collection-IntraDev/Intrexx_IntraDev_Datendrehscheibe|Intrexx_IntraDev_Datendrehscheibe]]