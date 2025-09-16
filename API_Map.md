```dataviewjs
const ROOT = "API_Endpoints";
const AREAS = ["IntraDev","Intranet"]; // weitere Bereiche möglich

const id = s => String(s).replaceAll(/[^A-Za-z0-9_]/g,"_");
const nameOf = p => p.split("/").pop().replace(/\.md$/,"");

// Alle relevanten Dateien einsammeln
const pages = dv.pages()
  .where(p => p.file.path.startsWith(ROOT + "/") && p.file.path.endsWith(".md"))
  .where(p => AREAS.some(a => p.file.path.startsWith(`${ROOT}/${a}/`)));

// Ordner -> Dateien
const byFolder = new Map();
for (const p of pages) {
  const fp = p.file.path;
  const folder = fp.substring(0, fp.lastIndexOf("/"));
  if (!byFolder.has(folder)) byFolder.set(folder, new Set());
  byFolder.get(folder).add(fp);
}

// alle Ordner (inkl. Zwischenordner) sammeln
const allFolders = new Set();
for (const f of byFolder.keys()) {
  const parts = f.split("/");
  for (let i=0; i<parts.length; i++){
    const sub = parts.slice(0,i+1).join("/");
    if (sub.startsWith(ROOT + "/")) allFolders.add(sub);
  }
}

// parent -> children
const children = new Map();
for (const f of allFolders) {
  const parent = f.substring(0, f.lastIndexOf("/"));
  if (parent && parent.startsWith(ROOT)) {
    if (!children.has(parent)) children.set(parent, new Set());
    children.get(parent).add(f);
  }
}

// Mermaid generieren
let out = [];
out.push("flowchart TB");
out.push(`subgraph ${id(ROOT)}["${ROOT}"]`);

function renderFolder(folder, indent="  ") {
  if (folder === ROOT) {
    for (const a of AREAS) {
      const sf = `${ROOT}/${a}`;
      if (allFolders.has(sf)) renderFolder(sf, indent);
    }
    return;
  }
  out.push(`${indent}subgraph ${id(folder)}["${folder.replace(ROOT + "/", "")}"]`);
  // Unterordner
  const kids = [...(children.get(folder) ?? [])].sort();
  for (const k of kids) renderFolder(k, indent + "  ");
  // Dateien direkt in diesem Ordner
  const files = [...(byFolder.get(folder) ?? [])].sort();
  for (const f of files) out.push(`${indent}  ${id(f)}["${nameOf(f)}"]`);
  out.push(`${indent}end`);
}
renderFolder(ROOT);
out.push("end"); // root subgraph

dv.paragraph("```mermaid\n" + out.join("\n") + "\n```");

```