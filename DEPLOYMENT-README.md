# Jimmy's Tapas Bar - Komplettes Deployment-Paket

## 📦 Inhalt des Pakets:

```
jimmys-tapas-bar/
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml         # Ein-Klick-Installation  
├── build-docker.sh           # Build-Script
├── UNRAID-INSTALLATION.md    # Unraid-Anleitung
├── backend/                  # FastAPI Backend
│   ├── server.py            # Hauptserver mit allen APIs
│   ├── requirements.txt     # Python-Dependencies
│   └── import_complete_menu_final.py  # Menü-Import (141 Artikel)
├── frontend/                 # React Frontend
│   ├── package.json         # Node-Dependencies
│   ├── src/                 # Source-Code
│   └── build/               # Produktions-Build
└── docker/                  # Docker-Konfiguration
    ├── nginx.conf           # Nginx-Proxy
    ├── supervisord.conf     # Service-Management
    ├── init-mysql.sql       # Datenbank-Schema
    └── start.sh             # Startup-Script
```

## 🚀 Installation auf Ihrem Server:

### Option 1: Docker Compose (Empfohlen)
```bash
# 1. Paket hochladen und entpacken
cd /home/your-user/
tar -xzf jimmys-tapas-deployment.tar.gz
cd jimmys-tapas-bar/

# 2. Container starten
docker-compose up -d
```

### Option 2: Einzelner Container
```bash
# 1. Image bauen
./build-docker.sh

# 2. Container starten
docker run -d \
  -p 80:80 \
  -p 8001:8001 \
  --name jimmys-tapas \
  --restart unless-stopped \
  jimmys-tapas:latest
```

### Option 3: Unraid Server
1. Docker-Image laden:
   ```bash
   docker load < jimmys-tapas-image.tar
   ```

2. In Unraid Container hinzufügen mit diesen Einstellungen:
   - **Repository:** `jimmys-tapas:latest`
   - **Host Port 80:** Container Port 80
   - **Host Port 8001:** Container Port 8001
   - **Volume:** `/mnt/user/appdata/jimmys-tapas/mysql` → `/var/lib/mysql`

## 🎯 Nach der Installation:

### 🌐 Website-Zugang:
- **Haupt-Website:** `http://IHR-SERVER-IP`
- **Admin-Panel:** `http://IHR-SERVER-IP/admin`

### 🔐 Admin-Login:
- **Username:** `admin`
- **Passwort:** `jimmy2024`

### ✅ Funktionen die automatisch funktionieren:

#### 🍽️ **Speisekarte:**
- 141 Menü-Artikel mit vollständigen Details
- MouseOver-Funktionalität für Gerichte-Details
- Kategorien: inicio, salat, tapas, pizza, pasta, dessert, getränke
- CMS-bearbeitbar (hinzufügen/bearbeiten/löschen)

#### 📱 **Content Management:**
- **Homepage:** Bearbeitbar über CMS
- **Standorte:** Neustadt & Großenbrode mit korrekten Adressen
- **Über uns:** Jimmy Rodríguez Geschichte ohne Team-Section
- **Kontaktformular:** Funktional mit schwarzer Schrift

#### 🛠️ **Admin-Funktionen:**
- **Benutzer-Verwaltung:** Accounts erstellen/bearbeiten
- **EU-Compliance:** DSGVO-Einstellungen (persistent)
- **Cookie-Management:** Cookie-Banner-Konfiguration (persistent)
- **Kontakt-Nachrichten:** Sammlung und Verwaltung

#### 🔧 **System:**
- **MySQL-Datenbank:** Persistent mit allen Daten
- **Nginx-Proxy:** Produktions-ready
- **Auto-Restart:** Container startet bei Server-Neustart
- **Health-Checks:** Automatische Überwachung

### 📊 **Daten-Persistierung:**
Alle Daten (Speisekarte, CMS-Einstellungen, Nachrichten) werden in Docker-Volumes gespeichert und bleiben bei Container-Updates erhalten.

### 🔄 **Updates:**
```bash
# 1. Neues Image pullen (wenn verfügbar)
docker-compose pull

# 2. Container neu starten
docker-compose up -d
```

## 💡 **Support:**
- **Entwickler:** Daniel Böttche
- **Tech-Stack:** React + FastAPI + MySQL
- **Architektur:** Docker Multi-Container Setup

**🎉 Jimmy's Tapas Bar ist produktions-bereit und vollständig einsatzfähig!**