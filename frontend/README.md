# Azure GenAI Chat – Deployment-Dokumentation

## 1. Architekturübersicht

Die Anwendung besteht aus:

* **Frontend:** React (Azure Static Web App)
* **Backend:** FastAPI (Azure Container Instance oder App Service, basierend auf Docker-Image)
* **Speicher:** Azure Storage Account (File Share für Zertifikate und Logs)
* **Netzwerkzugriff:** Azure Application Gateway als Reverse Proxy mit SSL/TLS
* **Zertifikat:** .pfx-Datei für HTTPS-Terminierung im Gateway

---

## 2. Voraussetzungen

* Azure CLI installiert und angemeldet
* Ressourcengruppe vorhanden: `AzureGenAIChat-RG`
* Storage Account: `azuregenaichatstorage`
* Docker-Image des Backends im Azure Container Registry oder auf Docker Hub

---

## 3. Schritte zur Bereitstellung

### Schritt 1: Erstellen des Storage Accounts und Hochladen des Zertifikats

```bash
az storage account create \
  --name azuregenaichatstorage \
  --resource-group AzureGenAIChat-RG \
  --location westeurope

export STORAGE_KEY=$(az storage account keys list \
  --resource-group AzureGenAIChat-RG \
  --account-name azuregenaichatstorage \
  --query "[0].value" -o tsv)

az storage share create --name reverseproxycerts \
  --account-name azuregenaichatstorage \
  --account-key $STORAGE_KEY

az storage file upload \
  --share-name reverseproxycerts \
  --source /reverse-proxy.pfx \
  --path reverse-proxy.pfx \
  --account-name azuregenaichatstorage \
  --account-key $STORAGE_KEY
```

---

### Schritt 2: Container Backend bereitstellen

Falls das Backend lokal als Container getestet wurde:

```bash
az container create \
  --name azure-genai-chat-aci \
  --resource-group AzureGenAIChat-RG \
  --image docker.io/<dein-image>:latest \
  --dns-name-label azure-genai-chat \
  --ports 8000
```

Nach erfolgreicher Bereitstellung prüfen:

```bash
az container show \
  --name azure-genai-chat-aci \
  --resource-group AzureGenAIChat-RG \
  --query ipAddress.fqdn -o tsv
```

Dieser FQDN wird im Application Gateway als Backendziel eingetragen.

---

### Schritt 3: Application Gateway erstellen

```bash
az network public-ip create \
  --resource-group AzureGenAIChat-RG \
  --name azure-genai-anwendungsgateway-pip \
  --sku Standard

az network vnet create \
  --resource-group AzureGenAIChat-RG \
  --name azuregenai-vnet \
  --subnet-name gateway-subnet

az network application-gateway create \
  --name azure-genai-anwendungsgateway \
  --location westeurope \
  --resource-group AzureGenAIChat-RG \
  --capacity 2 \
  --sku Standard_v2 \
  --vnet-name azuregenai-vnet \
  --subnet gateway-subnet \
  --frontend-port 443 \
  --public-ip-address azure-genai-anwendungsgateway-pip
```

---

### Schritt 4: Zertifikat binden und Listener konfigurieren

In der Azure Console:

1. Application Gateway → Listener → **HTTPS (443)**
2. Zertifikattyp: **PFX-Datei hochladen**
3. Pfad: `/reverse-proxy.pfx`
4. Kennwort: (aus `.env` oder lokalem Setup)
5. Backendziel: FQDN des Container-Backends
6. Backend-Port: 8000
7. Regel hinzufügen: Weiterleitung 443 → 8000

---

### Schritt 5: DNS-Eintrag

Optional kann eine eigene Domain auf die öffentliche IP des Gateways zeigen:

```bash
4.182.80.132  →  app.deinedomain.de
```

---

## 4. Fehlerbehebung

### 502 Bad Gateway

**Ursachen:**

* Backend nicht erreichbar (Container nicht läuft oder falscher Port)
* Backend-Health Probe im Gateway fehlerhaft
* TLS-Mismatch (falsches Zertifikat)
* Falscher FQDN oder Backendport in der Listenerregel

**Lösung:**

1. Container Logs prüfen:

   ```bash
   az container logs --name azure-genai-chat-aci --resource-group AzureGenAIChat-RG
   ```
2. Backend-Health in Application Gateway prüfen
3. Health Probe auf HTTP statt HTTPS setzen (wenn Backend HTTP ist)
4. Sicherstellen, dass Backend-Port = 8000 freigegeben ist

---

## 5. Überprüfung

Nach erfolgreichem Setup:

1. **Frontend (Static Web App)** → lädt über HTTPS von Application Gateway
2. **Gateway-Logs** → zeigen 200-Statuscodes
3. **Backend-Logs** → empfangen Requests korrekt
4. Browserzugriff über:

   ```
   https://4.182.80.132
   oder
   https://app.deinedomain.de
   ```
