


---

# API-Dashboard (Intranet ↔ IntraDev) – Anleitung

> [!tip] Zweck  
> Dieses Dashboard stellt APIs mit den Tags `#app/intranet` und `#app/intradev` **paarweise** gegenüber.  
> Ziel: Pro fachlicher API genau eine Zeile, mit Links zu beiden Umgebungen und einem Status („OK“/„FEHLT“).

## Wie wird gelistet?

- **Quelle**: Alle Notizen, die mindestens einen der Tags `#app/intranet` oder `#app/intradev` tragen.
    
- **Schlüsselbildung („key“)**
    
    - Wenn die Note ein Frontmatter-Feld `name:` hat, wird **dieser** Wert als Schlüssel verwendet.
        
    - Falls kein `name:` vorhanden ist, wird der **Dateiname** genutzt; ein evtl. Env-Suffix am Ende (`intranet` / `intradev`) wird entfernt.
        
- **Gruppierung**: Alle Notizen mit gleichem Schlüssel werden zu **einer Tabellenzeile** zusammengefasst.
    
- **Spalten**:
    
    - **API**: der Schlüssel (sichtbarer fachlicher Name).
        
    - **Intranet**: Link auf die Intranet-Variante (falls vorhanden).
        
    - **IntraDev**: Link auf die IntraDev-Variante (falls vorhanden).
        
    - **Status**: „OK“, wenn **beide** Varianten vorhanden sind; sonst „FEHLT“.
        

> [!tip] Best Practice
> 
> - Pflege **konsistente** `name:`-Werte in beiden Umgebungs-Notizen.
>     
> - Wenn ihr ohne `name:` arbeitet, achte darauf, dass der **Dateiname** bis auf das Env-Suffix identisch ist.
>     

> [!danger] Häufige Stolpersteine
> 
> - **Uneinheitliche Tags**: `#app/intraDev` vs. `#app/intradev` – Groß/Kleinschreibung ist egal, aber der **Text** muss gleich sein (empfohlen: `#app/intranet`, `#app/intradev`).
>     
> - **Env nicht am Dateinamen-Ende**: Das Suffix wird nur entfernt, wenn es **am Ende** steht. Wenn ihr „Foo.intranet.api.md“ habt, muss das Regex angepasst werden (siehe Hinweis unten).
>     
> - **Mehrere Notizen pro Env** mit gleichem Schlüssel: Die Tabelle zeigt nur **einen** Link pro Env; bereinige Dubletten.
>     

## Dataview-Snippet

```dataview
TABLE
  key AS "API",
  choice(length(filter(rows, (r) => contains(r.file.tags, "app/intranet"))) > 0,
         link(filter(rows, (r) => contains(r.file.tags, "app/intranet"))[0].file.link, "intranet"),
         "—") AS "Intranet",
  choice(length(filter(rows, (r) => contains(r.file.tags, "app/intradev"))) > 0,
         link(filter(rows, (r) => contains(r.file.tags, "app/intradev"))[0].file.link, "intradev"),
         "—") AS "IntraDev",
  choice(length(rows) = 2, "OK", "FEHLT") AS "Status"
FROM ""
WHERE contains(file.tags, "app/intranet") OR contains(file.tags, "app/intradev")
FLATTEN choice(name != null, name, file.name) AS raw
FLATTEN regexreplace(lower(raw), "[-_\\.\\s]*(intranet|intradev)$", "") AS key
GROUP BY key
SORT key ASC
```

> [!tip] Varianten & Anpassungen
> 
> - Ordner einschränken: Ersetze `FROM ""` durch `FROM "APIs"` o. ä.
>     
> - Env nicht am Ende? Nutze statt des letzten Regex:
>     
>     ```
>     FLATTEN regexreplace(lower(raw), "\\b(intranet|intradev)\\b", "") AS key
>     ```
>     
> - Lückenliste: Hänge unten an:
>     
>     ```
>     WHERE length(rows) < 2
>     ```
>     
>     (Zeigt nur APIs, bei denen Intranet **oder** IntraDev fehlt.)
>     

> [!danger] Wenn die Tabelle leer bleibt
> 
> - Prüfe, ob Dataview aktiviert ist und die Notizen **wirklich** die Tags `#app/intranet` / `#app/intradev` tragen.
>     
> - Prüfe, ob du im **eingestellten Vault-Bereich** suchst (Pfad im `FROM`).
>     
> - Entferne testweise alle `WHERE`/`FLATTEN`-Zeilen und füge sie wieder schrittweise hinzu, um den fehlerhaften Schritt zu identifizieren.
>     

---



#  Contract

> [!danger] API OVERVIEW
> **METHOD** `=upper(this.method)` · **AUTH** `=upper(this.auth)`
> ---
> **QUERY** _tbd_  
> **RESPONSE** _tbd_
Kurzfassung: Tags setzen → optional `name:` pflegen → Snippet einfügen → fertig.


```dataviewjs
const pages = dv.pages()
  .where(p => Array.isArray(p.file.tags) &&
    (p.file.tags.some(t => /app\/intranet/i.test(t)) || p.file.tags.some(t => /app\/intradev/i.test(t))));

const norm  = s => String(s).trim().toLowerCase();
const idify = s => norm(s).replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
const title = s => String(s).replace(/"/g, '\\"').replace(/\|/g, "\\|");

const map = new Map(); // key -> { name, intranet, intradev }
for (const p of pages) {
  const rawName = (p.name ?? p.file.name).replace(/\.(md|canvas)$/i, "");
  const key = norm(rawName.replace(/[-_.\s]*(intranet|intradev)$/i, "")); // Env-Suffix am Ende abschneiden
  const rec = map.get(key) || { name: rawName, intranet: null, intradev: null };
  if (p.file.tags.some(t => /app\/intranet/i.test(t))) rec.intranet = p.file.link;
  if (p.file.tags.some(t => /app\/intradev/i.test(t))) rec.intradev = p.file.link;
  map.set(key, rec);
}

let mer = [
  "graph LR",
  "classDef base fill:#ffffff,stroke:#555,stroke-width:1px,rx:6,ry:6",
  "classDef intranet fill:#e6ffe6,stroke:#2d6,stroke-width:1px,rx:6,ry:6",
  "classDef intradev fill:#e6eeff,stroke:#26c,stroke-width:1px,rx:6,ry:6",
  "classDef missing fill:#ffe6e6,stroke:#d22,stroke-width:2px,rx:6,ry:6"
];

for (const rec of map.values()) {
  const baseId = idify(rec.name);
  mer.push(`${baseId}["${title(rec.name)}"]:::base`);
  if (rec.intranet) {
    const n = baseId + "_intranet";
    mer.push(`${n}["intranet"]:::intranet --> ${baseId}`);
  } else {
    const n = baseId + "_intranet_missing";
    mer.push(`${n}["intranet fehlt"]:::missing -.-> ${baseId}`);
  }
  if (rec.intradev) {
    const n = baseId + "_intradev";
    mer.push(`${baseId} --> ${n}["intradev"]:::intradev`);
  } else {
    const n = baseId + "_intradev_missing";
    mer.push(`${baseId} -.-> ${n}["intradev fehlt"]:::missing`);
  }
}

dv.paragraph("```mermaid\n" + mer.join("\n") + "\n```");

```
