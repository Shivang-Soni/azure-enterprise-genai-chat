# Anfang mit einer offiziellen Python 3.10 x86_64 Image 
FROM --platform=linux/amd64 python:3.10.12-slim-bullseye

# Arbeitsverzeichtnis
WORKDIR /app

# Voraussetzungen werden kopiert
COPY requirements.txt .

# pip wird aktualisiert und Abhängigkeiten werden nachher installiert
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# App code wird kopiert
COPY . .

# .env Datei:
ENV $(cat .env | xargs)

# Portfreigabe
EXPOSE 8000

# Startbefehl für FastAPI mit uvicorn wird hier festgelegt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]