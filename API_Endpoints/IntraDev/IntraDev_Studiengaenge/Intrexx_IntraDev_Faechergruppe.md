---
type: api-endpoint
auth: "[[IntraDev_Key_Webkey]]"
title: Studiengänge — faechergruppe (IntraDev)
tags:
  - project/intrexx-rest-discovery
  - system/intrexx
  - app/intradev
  - env/dev
  - exposure/internal-nonprod
  - collection/studiengaenge
  - status/wip
  - spec/none
  - lang/de
  - endpoint/faechergruppe
  - method/get
  - status/active
owner: Team Integration
guid_hash: EC0FC1578BEB59BB5BA7B1A9C0102593E74FAB1F
base_url: "[[BaseURL_intraDev]]"
path_prefix: /api/app
path_entities:
  - /faechergruppe
method: GET
collection_ref: "[[Intrexx_Rest_Documentation/Collections/API-Collection-IntraDev/Intrexx_IntraDev_Studiengaenge|Intrexx_IntraDev_Studiengaenge]]"
last_checked: 2025-08-26
provider: provider
consumer: consumer
---


#  Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=this.auth`
---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
```dataviewjs
// ===== Konfig =====
const fm = dv.current().file.frontmatter;

// — Hilfen —
const isUrl = s => /^https?:\/\//i.test(String(s || ""));
const escPipes = s => String(s).replaceAll("|","\\|");

// [[Page]] oder [[Page|Alias]] aus String extrahieren
function unwrapWiki(s) {
  const m = String(s || "").match(/^\s*\[\[([^|\]]+)(?:\|[^]]*)?\]\]\s*$/);
  return m ? m[1] : String(s || "");
}

// base_url auflösen: unterstützt Link-Objekt, [[…]]-String oder Seitennamen/URL
function resolveBase(val) {
  if (!val) return "";
  // Obsidian/Dataview Link-Objekt
  if (typeof val === "object" && (val.path || val.file)) {
    const pg = dv.page(val.path ?? val.file);
    return (pg?.base_url ?? pg?.url ?? "").toString();
  }
  // String: evtl. [[…]] entfernen
  const raw = String(val);
  const s = unwrapWiki(raw);
  if (isUrl(s)) return s;                      // direkte URL
  const pg = dv.page(s);                       // Seite per Name/Path
  if (pg) return (pg.base_url ?? pg.url ?? "").toString();
  return s;                                    // Fallback: unverändert
}

// sauber joinen (ohne doppelte Slashes)
function joinUrl(...parts) {
  return parts
    .filter(p => p !== undefined && p !== null && String(p).trim() !== "")
    .map((p, i) => {
      const s = String(p).trim();
      if (i === 0) return s.replace(/\/+$/,"");
      return s.replace(/^\/+/,"").replace(/\/+$/,"");
    })
    .join("/");
}

// — Werte aus Frontmatter —
const base   = resolveBase(fm.base_url);
const prefix = fm.path_prefix ?? "";
const guid   = fm.guid_hash ?? "";
const method = String(fm.method ?? "").toUpperCase() || "GET";

// Entities sammeln (mehrere Key-Varianten)
let entities = [];
if (Array.isArray(fm.path_entities)) entities = fm.path_entities;
else if (Array.isArray(fm.entity_paths)) entities = fm.entity_paths;
else if (Array.isArray(fm.paths)) entities = fm.paths;
else if (fm.entity_path) entities = [fm.entity_path];
else if (fm.path) entities = [fm.path];

entities = entities.map(x => String(x ?? "").trim()).filter(Boolean);

// Hinweis, falls base leer oder nicht aufgelöst
const unresolved = !base || !isUrl(base);

// — Tabelle als Markdown in [!tip] rendern —
let md = [];
// Callout-Kopf (ersetzen)
md.push("> [!summary] ENDPOINT PREVIEW");
md.push(`> **METHOD** \`${method}\`` + (unresolved ? " · **BASE** `unresolved`" : ""));
md.push("> ---");  // dünne Trennlinie

// Tabellenkopf
// Tabellenkopf (lassen wir, nur techy Bezeichnung)
md.push("> | PATH | TEMPLATE & URL | TEST |");
md.push("> |---|---|:--:|");

// Zeilen
for (const rawSeg of entities) {
  const seg = escPipes(rawSeg);
  const template = escPipes(joinUrl("base_url", "path_prefix", "guid_hash", rawSeg));
  const url = unresolved ? "" : joinUrl(base, prefix, guid, rawSeg);

  const detailsCell = url
    ? `\`${template}\`<br><code>${escPipes(url)}</code>`
    : `\`${template}\``;

  const testCell = url ? `[${method}](${url})` : "—";

  md.push(`> | \`${seg}\` | ${detailsCell} | ${testCell} |`);
}

// Ausgabe
dv.paragraph(md.join("\n"));

```

```dataviewjs
// ===== TECHY RELATIONS CALLOUT (no emojis) =====
const fm = dv.current().file.frontmatter;

// --- Helpers ---
function unwrapWiki(s) {
  const m = String(s || "").match(/^\s*\[\[([^|\]]+)(?:\|[^]]*)?\]\]\s*$/);
  return m ? m[1] : String(s || "");
}
function pageFrom(val) {
  if (!val) return null;
  if (typeof val === "object" && (val.path || val.file)) return dv.page(val.path ?? val.file) ?? null;
  const s = unwrapWiki(String(val));
  return dv.page(s) 
      ?? dv.pages().where(p => String(p.file?.name) === s 
         || (Array.isArray(p.file?.aliases) && p.file.aliases.some(a => String(a) === s))).first()
      ?? null;
}
function linkify(val) {
  const pg = pageFrom(val);
  if (pg?.file?.path) return `[[${pg.file.path}|${pg.file.name}]]`;
  const s = unwrapWiki(val);
  return s ? `\`${s}\`` : "—";
}
function asArray(v) { return Array.isArray(v) ? v : (v ? [v] : []); }

// --- Collect relations ---
const parentsRaw = asArray(fm.collection_ref);
const parentLinks = parentsRaw.map(linkify);

// Siblings: andere Seiten, die denselben Parent referenzieren
let sibs = [];
for (const pr of parentsRaw) {
  const target = pageFrom(pr);
  const key = target?.file?.path ?? unwrapWiki(pr);
  if (!key) continue;
  const matches = dv.pages()
    .where(p => p.file?.path !== dv.current().file.path)
    .where(p => {
      const cr = asArray(p.collection_ref);
      return cr.some(x => {
        const pg = pageFrom(x);
        const k = pg?.file?.path ?? unwrapWiki(x);
        return k && k === key;
      });
    })
    .sort(p => p.file.name, 'asc')
    .array();
  sibs.push(...matches);
}
// Dedup by file.path
const seen = new Set();
const siblings = sibs.filter(p => {
  const k = p.file?.path ?? p.file?.name;
  if (seen.has(k)) return false; seen.add(k); return true;
});

// --- Render (techy) ---
// --- Render (techy, einheitlich) ---
let md = [];
md.push("> [!abstract] RELATIONS");
md.push("> ");
md.push("> **PARENT**");
md.push(`> ${parentLinks.length ? parentLinks.join("  ") : "—"}`);
if (siblings.length) {
  md.push("> ---");
  md.push(`> **SIBLINGS** (${siblings.length})`);
  for (const s of siblings) md.push(`> - [[${s.file.path}|${s.file.name}]]`);
}
md.push("> ");
md.push("> source: `collection_ref`");
dv.paragraph(md.join("\n"));



```