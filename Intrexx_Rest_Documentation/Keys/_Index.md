---
type: key-index
title: "API Keys — Index"
tags:
  - project/intrexx-rest-discovery
  - auth/key
  - status/active
---

# API Keys — Übersicht

> Optional mit Dataview (falls Plugin installiert):
```dataview
TABLE key_id, key_type, file.link AS key_note, owner, env, join(scopes,", ") AS scopes, rotation_policy, last_rotated, expires_at, tags
FROM "Intrexx_Rest_Documentation/Keys"
WHERE type = "key"
SORT expires_at ASC
