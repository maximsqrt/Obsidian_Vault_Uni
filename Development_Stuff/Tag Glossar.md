---
title: Tag Glossar
---
```dataviewjs
// Tag → Beschreibung (Beispiel)
const DESC = {
  "status/active":     "Produktiv freigegeben.",
  "status/wip":        "In Arbeit; noch nicht stabil.",
  "status/deprecated": "Veraltet, bitte migrieren.",
  "status/http-4xx":   "Clientfehler bei letzter Prüfung.",
  "status/http-5xx":   "Serverfehler bei letzter Prüfung."
};

// Hilfsfunktion: klickbarer Tag-Link (ohne Markdown-Parsing)
function tagLink(t) {
  const q = encodeURIComponent("tag:" + t);
  // dv.el(tagName, text, attrs) -> HTMLElement
  return dv.el("a", "#" + t, { href: `obsidian://search?query=${q}` });
}

dv.table(
  ["Tag", "Beschreibung"],
  Object.entries(DESC).map(([t, d]) => [tagLink(t), d])
);

```
