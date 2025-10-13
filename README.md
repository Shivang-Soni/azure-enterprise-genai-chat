# Azure Enterprise GenAI Chat

**Enterprise-fähiger KI-Chatbot mit FastAPI und Azure-Diensten**

Dieses Projekt demonstriert eine **Azure-native, skalierbare KI-Lösung**, die sofort in Azure deploybar ist. Es kombiniert:

- **FastAPI** als moderne, performante API  
- **Azure Cognitive Search** für kontextbasierte Suche  
- **Azure OpenAI (GPT-Integration)** für intelligente Antworten  
- **Azure Blob Storage** für Dokumentenablage  
- **Azure Key Vault** für sichere Secrets & Konfiguration  
- RBAC- und Audit-ready Struktur  

## Funktionen
- Chat-Endpoint `/chat` mit GPT & Search-Kontext  
- Async-API für Enterprise-Performance  
- Demo-Notebook `notebooks/demo.ipynb` mit Beispiel-Daten  
- Dockerfile für einfache Deployment-Optionen  
- `.env.example` für lokale Entwicklung / Azure Keys  

## Architektur
[User] --> [FastAPI App] --> [Cognitive Search / OpenAI / Blob Storage] --> [Antwort]

## Deployment
1. Azure App Service / Container-Instance  
2. Setze die Environment-Variablen:
   - `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`  
   - `AZURE_OPENAI_ENDPOINT`  
   - `AZURE_BLOB_CONNSTRING`  
   - `AZURE_KEYVAULT_URL`  
3. Starte die API lokal:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Demo
POST /chat
{
  "query": "Wie unterstützt Genoverband e.V. seine Mitglieder?"
}
Antwort enthält GPT-generierte Antwort + relevante Dokumente aus Search.