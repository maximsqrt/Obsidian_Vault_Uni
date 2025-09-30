
```dataview
TABLE WITHOUT ID t AS Tag, length(rows) AS Count
FROM ""
FLATTEN file.tags AS t
GROUP BY t
SORT Count DESC
```
```dataviewjs
const map = dv.current().tag_descriptions ?? {};
const counts = {};
for (const p of dv.pages("")) for (const tag of (p.file.tags ?? [])) {
  const t = String(tag).replace(/^#/,""); counts[t]=(counts[t]||0)+1;
}
dv.table(["Tag","Beschreibung","Count"],
  Object.entries(counts)
    .sort((a,b)=>b[1]-a[1])
    .map(([t,c]) => [`#${t}`, map[t] ?? "", c]));
```
