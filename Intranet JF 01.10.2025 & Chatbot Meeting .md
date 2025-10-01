


Alles Wesentliche — auf ~50 % gekürzt und **nach Wichtigkeit priorisiert**.

# Top-Fragen (priorisiert)

1. **Mandant & Zugriff**
    

- Gibt es stabile IDs für **Projekt (= Kunde)** und **Group (= Botname)** (`project_id`, `group_id`)?
    
- Sind Sammlungen strikt pro Projekt isoliert? Rollen/Token (Owner/Writer/Reader)?
    

2. **Sammlung (Collection) anlegen & adressieren**
    

- Anlage via API? Rückgabe von `collection_id` + sprechendem `collection_slug`?
    
- Lebenszyklus: Umbenennen/Archivieren/Löschen – Auswirkungen auf Dokumente/Chunks?
    

3. **Upload & Idempotenz (einmalig hochladen)**
    

- Unterstützte Formate (PDF/DOCX/TXT/MD/CSV/HTML) und Max-Größe?
    
- `external_id` + Content-Hash → Duplikaterkennung/Idempotenz?
    
- Pflicht-Metadaten: `title`, `language`, `doctype`, `tags`, `effective_date`, `custom_kv`?
    

4. **Chunking (Qualität & Stabilität)**
    

- Strategie/Parameter: `max_tokens`, `overlap_tokens`, header-aware/sentence-aware?
    
- Stabilität der **Chunk-IDs** bei identischem Inhalt (für Caching/Vektoren)?
    
- Persistenz von Offsets/Seiten/Absatz-IDs für Zitatgenauigkeit?
    

5. **Corpus/Index-Zuordnung**
    

- Wird `corpus_id` explizit je Upload übergeben oder aus Sammlung abgeleitet?
    
- Mehrfache Indizierung eines Dokuments in mehrere Corpora – atomar/synchron?
    

6. **Indexierung & Jobs**
    

- Sync vs. Async Build; Job-Status/Progress-Endpoint; Fehler-Retry/Dead-letter?
    

7. **Updates & Versionierung (bearbeitete Dokumente)**
    

- Policy: **Überschreiben**, **Versionieren**, oder **Dual parallel**?
    
- Atomarer Switch (blue/green) der Chunks im Index?
    
- Beibehalt der `document_id` beim Überschreiben?
    

8. **Löschung & Retention**
    

- Delete-Semantik: entfernt auch Chunks/Embeddings (hard) oder Tombstone (soft)?
    
- DSGVO/Retention-Regeln je Sammlung; Audit-Trail erforderlich?
    

9. **Metadaten/Taxonomie & Ranking**
    

- Einheitliches Schema je Sammlung; Validierung von Pflichtfeldern?
    
- Filter/Facetten (`doctype`, `language`, `effective_date`, `confidentiality`, `project`, `group`)?
    
- Metadata-Boosting im Ranking/HYBRID (BM25+Vector)?
    

10. **Retrieval-Grenzen & Relevanz**
    

- Query-Limits, Top-k, Max-Kontextlänge für Bot; Cross-Collection-Query erlaubt?
    
- Antwort-Attribution: Rückgabe von `document_id`, `chunk_id`, Offsets/Seiten.
    

---

# Minimale API-Shapes (kompakt)

**Sammlung anlegen**

```http
POST /v1/collections
{ "project_id": "...", "group_id": "...", "name": "Policies-2025", "slug": "policies-2025",
  "chunking": { "max_tokens": 800, "overlap_tokens": 100, "mode": "header_aware" } }
→ { "collection_id": "col_123", "slug": "policies-2025" }
```

**Dokument hochladen (+ Corpus)**

```http
POST /v1/documents
{ "project_id":"...", "group_id":"...", "collection_id":"col_123",
  "external_id":"cust-42:handbuch-v3", "title":"Handbuch v3.pdf",
  "corpus_id":"corp_main", "metadata":{ "doctype":"manual","language":"de" },
  "file": "<multipart-binary>" }
→ { "document_id":"doc_789", "chunks": "queued", "job_id":"job_abc" }
```

**Update-Policy steuern**

```http
POST /v1/documents/ingest
{ "external_id":"cust-42:handbuch-v3", "update_policy":"overwrite" | "version" | "dual",
  "atomic_switch": true }
```

**Job-Status**

```http
GET /v1/jobs/job_abc
→ { "status":"completed", "indexed_chunks": 1240 }
```

**Delete**

```http
DELETE /v1/documents/doc_789?mode=hard
→ { "status":"deleted" }
```

---

# Use Case „Dokuanbindung“ (präzise)

- **Ziel:** Einmaliger Upload kundenbezogener Dokumente in eine projektspezifische Sammlung; automatisches Chunking; Indizierung in definiertem Corpus; deterministische Updates (Overwrite/Version/Dual); sauberes Retrieval mit Attribution.
    
- **Mandantenmodell:** `project_id` = Kunde, `group_id` = Botname. Jede Sammlung gehört genau einem Projekt; Zugriff über rollenbasierte Token.
    
- **Betrieb:** Async-Indexierung mit Job-Status; atomare Umschaltung bei Updates; vollständige Auditierbarkeit; DSGVO-konforme Löschung.
    

Wenn du willst, passe ich die Parameter (Chunk-Größen, Update-Policy, Schemas) direkt auf eure Dokus an und liefere OpenAPI-konforme Specs.