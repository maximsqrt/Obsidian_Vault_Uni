---
aliases: [APIs_intraDev]
tags: [api, index]
---

# APIs – intraDev (gefiltert nach base_url = [[BaseURL_intraDev]])

```dataviewjs
// === Konfiguration ===
const BASE_NOTE  = "BaseURL_intraDev";                        // Wikilink-Note
const BASE_HOSTS = ["intradev.zv.uni-freiburg.de"];           // Fallback: rohe URL-Varianten
const PATH_FIELDS = ["endpoint","path","url_path","api","route"];

// === Helpers ===
const getMethod = p => {
  if (p.method) return String(p.method).toUpperCase();
  const tag = (p.file?.tags ?? []).find(t => /^method\/\w+$/i.test(t));
  return tag ? tag.split("/")[1].toUpperCase() : "";
};
const getEndpoint = p => {
  for (const k of PATH_FIELDS) if (p[k]) return String(p[k]);
  return p.file.name;
};
const isApiNote = p =>
  p.file?.ext === "md" && (
    !!p.method ||
    (p.file?.tags ?? []).some(t => /^method\/\w+$/i.test(t))
  );

// base_url kann Link oder String sein → robust prüfen
function matchesBase(p){
  const v = p.base_url ?? p["base-url"];
  if (!v) return false;
  // Wikilink-Objekt?
  if (typeof v === "object" && v.path) {
    // v.path ist z. B. "BaseURL_intraDev" oder "SomeFolder/BaseURL_intraDev"
    return v.path.toLowerCase().includes(BASE_NOTE.toLowerCase());
  }
  const s = String(v).toLowerCase();
  if (s.includes(BASE_NOTE.toLowerCase())) return true;             // [[BaseURL_intraDev]]
  return BASE_HOSTS.some(h => s.includes(h.toLowerCase()));         // nackte URL
}

// === Abfrage & Ausgabe ===
const rows = dv.pages()
  .where(isApiNote)
  .where(matchesBase)
  .sort(p => getEndpoint(p), 'asc')
  .map(p => [getMethod(p), getEndpoint(p), p.file.link, p.base_url ?? p["base-url"] ?? ""]);

dv.table(["Method", "Endpoint", "Note", "Base"], rows);
