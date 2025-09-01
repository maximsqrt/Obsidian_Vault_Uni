---
aliases:
color: ""
---

# Fix Endpoints 

```dataview
TABLE without ID link(file.link, ressource) as Task, path
FROM "Endpoints"
WHERE status = "broken"
```


```dataview
LIST
FROM "Endpoints"
WHERE status = "broken"
```


```dataview
TASK
FROM "Endpoints"
```



#TODO BALBLAC

Idee 
eine datei Aufgaben die automatisch aus allen files (moentan endpoints) via properties status broken filtert und anzegt und 

andere idee zb checkboxen sammeln von allen 

grundsätzich apis doku sollte automatisch aus dem code genereirt

eigentlich sollte es sowas geben wie [[BaseURL_Intranet]]/api/app/56E423A507C34F76FD114442921B0AF44BA57B88/fundsachen/DOCS



haben ir ja! irgendwie die API docs hier holen 



Rust aufgabe: 
nimm die API DOC von intrexx crawlen und markdown fileZ bauen. 