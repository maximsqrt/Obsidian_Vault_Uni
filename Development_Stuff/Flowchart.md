## API-Struktur

```mermaid
flowchart TB
  %% Root
  root["API_Endpoints"]

  %% --- IntraDev ---
  subgraph sg_intradev["IntraDev"]
    direction TB
    intradev_anchor["IntraDev"]
    intradev_a["Endpoint A (---)"]
    intradev_b["Endpoint B"]
    intradev_c["Endpoint C"]
    %% Verzweigungen unter IntraDev
    intradev_anchor --> intradev_a
    intradev_anchor --> intradev_b
    intradev_anchor --> intradev_c

    %% Beispiel: weitere Tiefe unter einem Knoten
    intradev_a --> intradev_a1["A → Sub 1"]
    intradev_a --> intradev_a2["A → Sub 2"]
  end

  %% --- Intranet ---
  subgraph sg_intranet["Intranet"]
    direction TB
    intranet_anchor["Intranet"]
    intranet_x["Service X"]
    intranet_y["Service Y"]
    intranet_z["Service Z"]
    %% Verzweigungen unter Intranet
    intranet_anchor --> intranet_x
    intranet_anchor --> intranet_y
    intranet_anchor --> intranet_z

    %% Beispiel: weitere Tiefe unter einem Knoten
    intranet_x --> intranet_x1["X → Sub 1"]
  end

  %% Top-Level Kanten
  root --> intradev_anchor
  root --> intranet_anchor
