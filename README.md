```markdown
# Azure Enterprise GenAI Chat

**Enterprise-fähiger KI-Chatbot mit FastAPI und Azure-Diensten**

Dieses Projekt demonstriert eine **Azure-native, skalierbare KI-Lösung**, die sofort in Azure deploybar ist. Es kombiniert:

- **FastAPI** als moderne, performante API  
- **Azure Cognitive Search** für kontextbasierte Suche  
- **Azure OpenAI (GPT-Integration)** für intelligente Antworten  
- **Azure Blob Storage** für Dokumentenablage  
- **Azure Key Vault** für sichere Secrets & Konfiguration  
- RBAC- und Audit-ready Struktur  

---

## Funktionen

- Chat-Endpoint `/api/chat` mit GPT & Search-Kontext  
- Asynchrone API für Enterprise-Performance  
- React ChatBot Frontend (`frontend/`) mit:
  - Chat-UI, automatischem Scrollen und Ladeindikator
  - Input-Feld für Benutzerfragen
  - POST Requests an `/api/chat`, konfigurierbar via `REACT_APP_API_URL`
- Demo-Notebook `notebooks/demo.ipynb` mit Beispiel-Daten  
- Dockerfile für einfache Deployment-Optionen  
- `.env.example` für lokale Entwicklung / Azure Keys  

---

## Architektur

```

[User / Browser]
│ HTTPS 443
▼
[Application Gateway / Frontend-IP]
│ Weiterleitung an Backend-IP 10.0.1.5
▼
[Nginx Reverse Proxy Container]
│ HTTP/HTTPS intern
▼
[FastAPI App Container / Azure App Service]
│ Zugriff auf Azure OpenAI, Cognitive Search, Blob Storage

````

---

## Azure VNet & Application Gateway

### Virtuelles Netzwerk (VNet)

- Name: `azure-genai-chat-vnet`  
- Subnetze:
  - **Frontend-Subnet** (`10.0.2.0/24`) → Application Gateway  
  - **Backend-Subnet** (`10.0.1.0/24`) → FastAPI / Nginx Container  

### Application Gateway

- Typ: Layer 7 Load Balancer / Reverse Proxy  
- Frontend-IP: öffentlich  
- Back-End Pool: IP von Nginx Container im Backend-Subnet (`10.0.1.5`)  
- Listener: HTTPS, Port 443  
  - Zertifikat: self-signed (Dev-Test) oder Managed CA (Produktion)  
- Routing-Regeln:
  - `/api/*` → Weiterleitung an Nginx/FastAPI im Backend  
  - `/` → optional React Static Web App  

### Nginx Reverse Proxy (Backend)

- Container-IP: `10.0.1.5`  
- Leitet Traffic vom Application Gateway an FastAPI weiter  
- HTTPS optional für internes Routing  

---

## Deployment

### 1. Azure Deployment

- App Service oder Container-Instance im VNet  
- Optional: Azure Application Gateway für HTTPS  
- SSL: 
  - Dev-Test: self-signed Zertifikat akzeptieren  
  - Produktion: Azure Managed Certificate oder CA-Zertifikat

### 2. Environment-Variablen setzen

```bash
AZURE_SEARCH_ENDPOINT=<your-search-endpoint>
AZURE_SEARCH_KEY=<your-search-key>
AZURE_OPENAI_ENDPOINT=<your-openai-endpoint>
AZURE_OPENAI_KEY=<your-openai-key>
AZURE_BLOB_CONNSTRING=<your-blob-connection-string>
AZURE_KEYVAULT_URL=<your-keyvault-url>
REACT_APP_API_URL=https://<frontend-url>/api/chat
````

### 3. Backend lokal starten

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend lokal starten

```bash
cd frontend
npm install
npm start
```

---

## Sicherheit

* Secrets werden ausschließlich über Key Vault gelesen
* CORS: für SWA Deployment erlaubt `allow_origins=["*"]`
* SSL / HTTPS: self-signed Zertifikat für Dev-Test möglich, für Produktion unbedingt CA-Zertifikat verwenden

---

## Hinweise für Testing (Dev)

1. Öffne im Browser `https://4.182.80.132`
2. Bei Warnung „Ihre Verbindung ist nicht privat“ → **Erweitert → Trotzdem fortfahren**
3. React fetch POST an `/api/chat` funktioniert danach ohne Fehler
4. Alternativ: Zertifikat dauerhaft im System als vertrauenswürdig installieren

---

## Docker (optional)

```bash
docker build -t azure-genai-chat .
docker run -p 8000:8000 azure-genai-chat
```

---

## Hinweise

* Für Produktion: Azure Managed Certificate installieren → keine Browser-Warnungen
* Skalierbar über Azure App Service / Container Instances / VNet
* Logging, Monitoring und RBAC für Enterprise-ready Betrieb vorbereitet

```
```
