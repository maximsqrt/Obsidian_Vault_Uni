
---

# REST-API Doku (Obsidian Vault)

Dieses Repository enthält den **Obsidian Vault** mit der vollständigen REST-API-Dokumentation für:

* **Intranet**
* **IntraDev**
* **OData** (teilweise nicht mehr aktiv)

Die Dokumentation ist **.md-/Plaintext-basiert** und wird im Vault in einer sauberen Ordnerstruktur gepflegt. Für die **detailreiche Nutzung und Navigation** wird **Obsidian** empfohlen:
👉 [https://obsidian.md/](https://obsidian.md/)

Eine **vereinfachte** (kompaktierte) Doku der wichtigsten Endpunkte findet sich zusätzlich im Wiki:
👉 [https://gitlab.rz.uni-freiburg.de/intranet/intranet-allgemein/-/wikis/RESTV2?edit=true](https://gitlab.rz.uni-freiburg.de/intranet/intranet-allgemein/-/wikis/RESTV2?edit=true)

---

## Inhalt

* [Ziele & Scope](#ziele--scope)
* [Voraussetzungen](#voraussetzungen)
* [Ordnerstruktur](#ordnerstruktur)
* [Frontmatter–Schema (YAML)](#frontmatter-schema-yaml)
* [Status & Stage-Badges](#status--stage-badges)
* [Tabellen-Generierung (overview.md)](#tabellen-generierung-overviewmd)
* [Workflows](#workflows)
* [Konventionen](#konventionen)
* [Troubleshooting](#troubleshooting)
* [Contribution](#contribution)

---

## Ziele & Scope

* **Single Source of Truth**: Alle REST-Schnittstellen (Intranet, IntraDev, OData) liegen konsistent im Obsidian Vault.
* **Maschinenlesbar + menschenlesbar**: Jede API-Seite besitzt YAML-Frontmatter für Tools und sauberes Rendern.
* **Schneller Überblick**: Automatisch generierte Tabellenübersicht in `registry/overview.md` (inkl. Method, Base, Stage, Spec, guid\_hash, path\_entities).

---

## Voraussetzungen

* **Python 3.10+**
* Abhängigkeiten (lokal im Repo gepflegte Skripte nutzen nur Standardlibs; falls PyYAML nötig ist):

  ```bash
  pip install pyyaml
  ```
* **Obsidian** (empfohlen für die tägliche Arbeit mit dem Vault): [https://obsidian.md/](https://obsidian.md/)

---

## Ordnerstruktur

```text
.
├─ registry/
│  ├─ apis.yml              # Sammel-Registry (Export/Build-Zwischenergebnis)
│  ├─ overview.md           # automatisch generierte Tabellen-Übersicht
│  └─ ...                   # ggf. weitere Registry-Artefakte
├─ scripts/
│  ├─ yaml_to_md.py         # erzeugt overview.md aus registry/apis.yml
│  ├─ export_registry.py    # (optional) baut apis.yml aus Frontmatter-Scans
│  ├─ export_functions.py   # (optional) weitere Exporte
│  └─ ...
├─ intranet/                # API-Dokumente (Markdown) mit YAML-Frontmatter
├─ intradev/                # dito
├─ odata/                   # teilweise inaktiv, als historischer Kontext
└─ README.md
```

> **Hinweis:** Die Namen können lokal abweichen; wichtig ist, dass `scripts/yaml_to_md.py` die `registry/apis.yml` findet (siehe unten).

---

## Frontmatter–Schema (YAML)

Jede API-/Endpoint-Datei beginnt mit YAML-Frontmatter. Minimalbeispiel:

```yaml
---
name: Benutzerverwaltung
family: intranet
stage: Beta
tags:
  - status/active
base: /v2/users/{userId}
auth: bearer
spec: https://intranet.example/api/users/openapi.json
method: GET
guid_hash: 1a2b3c4d         # optional; wird sonst aus guid/app_guid abgeleitet
path_entities:              # optional; wird sonst aus base/path extrahiert
  - userId
owner: Team Intranet        # optional (oder owner_ref)
app_guid: 8c9e...           # optional
---
```

**Pflicht für Aufnahme in die Übersicht:** `tags` enthält `status/active`.

**Felder – Kurzüberblick**

* `name`: Anzeigename der Schnittstelle/Resource
* `family`: `intranet`, `intradev`, `odata` (wird in der Übersicht gruppiert)
* `stage`: `Dev` | `Alpha` | `Beta` | `GA` | `Prod` | `Deprecated`
* `base`: Basis-Pfad (z. B. `/v2/users/{userId}`)
* `auth`: z. B. `bearer`, `basic`, `session`
* `spec`: Link auf OpenAPI/Swagger oder interne Spezifikation
* `method` | `methods`: HTTP-Methode(n)
* `guid_hash`: kurzer Hash als Referenz (8 Zeichen), alternativ `guid`/`app_guid`
* `path_entities`: Platzhalter im Pfad (z. B. `userId`)
* `owner` | `owner_ref`: organisatorischer Owner

---

## Status & Stage-Badges

Die Übersicht rendert eine Stage-Badge pro Eintrag:

| Stage      | Badge-Farbe (Shields.io) |
| ---------- | ------------------------ |
| GA / Prod  | brightgreen              |
| Beta       | yellow                   |
| Alpha      | orange                   |
| Dev        | blue                     |
| Deprecated | lightgrey                |

Nur Einträge mit `status/active` werden gelistet.

---

## Tabellen-Generierung (`overview.md`)

Die Datei `registry/overview.md` wird aus `registry/apis.yml` generiert.

### 1) YAML bereitstellen

* Variante A: **Export/Scan** erzeugt `registry/apis.yml` (z. B. via `export_registry.py`).
* Variante B: `apis.yml` manuell pflegen (Konform zum Frontmatter-Schema).

Beispielstruktur `apis.yml` (verkürzt):

```yaml
apis:
  - name: Benutzerverwaltung
    family: intranet
    stage: Beta
    base: /v2/users/{userId}
    auth: bearer
    spec: https://.../openapi.json
    method: GET
    guid_hash: 1a2b3c4d
    path_entities: [userId]
```

### 2) Übersicht generieren

Das Skript **läuft ohne Argumente** (VS-Code „Run Code“ kompatibel) und sucht automatisch nach `../registry/apis.yml` bzw. `./registry/apis.yml`.

* **Standardlauf (flache Tabelle)**
  Start per „Run Code“ in VS Code **oder** im Terminal:

  ```bash
  python scripts/yaml_to_md.py
  ```

  Ergebnis: `registry/overview.md` (Spalten: API, Base, Auth, Stage, Spec, Method, guid\_hash, path\_entities)

* **Optionale Flags (Terminal):**

  * `--grouped` – gruppiert nach `family` (IntraDev/Intranet/OData/Rest)
  * `--owner` – blendet die Spalte „Owner“ zusätzlich ein

  ```bash
  python scripts/yaml_to_md.py --grouped --owner
  ```

---

## Workflows

### Neuer Endpoint

1. Neue Markdown-Datei im passenden Ordner (`intranet/…`, `intradev/…` etc.).
2. YAML-Frontmatter gemäß Schema eintragen (inkl. `status/active`).
3. Export/Build anstoßen (falls `apis.yml` aus den Dateien generiert wird).
4. `scripts/yaml_to_md.py` ausführen → `registry/overview.md` aktualisiert sich.

### Pflege bestehender Einträge

* Felder in Frontmatter anpassen (z. B. Stage von `Beta` → `GA`, `owner`, `spec`-Link).
* Bei Pfadänderungen (`base`) werden `path_entities` automatisch extrahiert, sofern nicht explizit gesetzt.

---

## Konventionen

* **Familien:** exakt `intranet`, `intradev`, `odata` (klein).
* **Stage:** `Dev` | `Alpha` | `Beta` | `GA` | `Prod` | `Deprecated`.
* **Methoden:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE` (einzeln oder Liste).
* **Platzhalter im Pfad:** `{userId}` oder `:userId` – beide werden erkannt.
* **Owner:** Klartext oder Referenz (z. B. Jira/Team-Alias).
* **Guid/Hash:** `guid_hash` kurz halten (8 Zeichen). Falls `guid`/`app_guid` vorhanden, wird im Build ein Short-Hash erzeugt.

---

## Troubleshooting

* **„tempCodeRunnerFile.py“/Inhalt „ren“**
  VS-Code „Run Selection“ hat nur einen Ausschnitt ausgeführt. Lösung: Nichts markieren und „Run Python File“ nutzen **oder** `code-runner.ignoreSelection=true`.

* **Zeilenende-Warnungen (CRLF/LF)**
  `.gitattributes` erzwingt LF für Code/Markdown/YAML. Einmal normalisieren:

  ```bash
  git add --renormalize .
  git commit -m "Normalize line endings"
  ```

* **Committer-Identität**

  ```bash
  git config --global user.name  "Vorname Nachname"
  git config --global user.email "you@example.com"
  ```

* **Obsidian-Wikilinks (`[[...]]`) in Tabellen**
  Werden in Code-Spans gerendert (Backticks). Links in `spec` werden als Markdown-Links ausgegeben.

---

## Contribution

* **PR-Style:** kleine, fokussierte Änderungen; aussagekräftige Commit-Messages.
* **Lint/Checks:** YAML syntaktisch valide halten, keine „toten“ Links in `spec`.
* **Review:** Stage-Änderungen und `Deprecated` kennzeichnen, Owner aktuell halten.
* **Merge-Policy:** Workspace-Dateien (`.obsidian/workspace.json`) werden per `merge=ours` lokal bevorzugt (siehe `.gitattributes`).

---

**Kontakt / Maintainer**
Bitte im jeweiligen GitLab-Projekt einen Issue öffnen oder den Owner der betroffenen API im Frontmatter ansprechen.
