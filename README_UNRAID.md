# 🌶️ Jimmy's Tapas Bar - Website für Unraid Docker

Eine vollständige statische Website für Jimmy's Tapas Bar mit 243 Menüpunkten, professionellem Design und allen lokalen Bildern.

## 🚀 SCHNELLSTART (für Unraid):

### **Option 1: Automatisches Setup (Empfohlen)**
```bash
chmod +x setup-unraid.sh
./setup-unraid.sh
```

### **Option 2: Docker Compose**
```bash
docker-compose up -d
```

### **Option 3: Manuell**
```bash
docker build -t jimmys-tapas-bar:latest .
docker run -d --name jimmys-tapas-bar --restart unless-stopped -p 8080:80 jimmys-tapas-bar:latest
```

## 📋 WAS IST ENTHALTEN:

✅ **Vollständige statische Website** (HTML/CSS/JS)
✅ **243 Menüpunkte** in 32 Kategorien
✅ **Alle Bilder lokal** gespeichert (keine externen Dependencies)
✅ **Professionelles Design** mit authentischen spanischen Bildern
✅ **Responsive Design** für alle Geräte
✅ **Kontaktformular** mit mailto-Funktionalität
✅ **Google Bewertungen** Integration
✅ **Optimierte Ladezeiten** durch lokale Assets

## 🌐 NACH DER INSTALLATION:

**Website öffnen:** `http://[UNRAID_IP]:8080`

## 📁 WICHTIGE DATEIEN:

- `UNRAID_INSTALLATION.md` - Detaillierte Installations-Anleitung
- `Dockerfile` - Optimiert für nginx mit statischen Dateien
- `docker-compose.yml` - Alternative Installation mit Compose
- `setup-unraid.sh` - Automatisches Setup-Script
- `config/menu.ini` - Speisekarte mit allen 243 Artikeln

## 🔧 ANPASSUNGEN:

- **Speisekarte ändern**: Bearbeiten Sie `config/menu.ini`
- **Bilder austauschen**: Ersetzen Sie Dateien in `images/`
- **Texte ändern**: HTML-Dateien in `pages/` bearbeiten

## 📊 SYSTEM-ANFORDERUNGEN:

- **RAM**: 256MB
- **Storage**: 50MB
- **Ports**: 1 freier Port (Standard: 8080)

**🎉 Viel Erfolg mit Ihrer Jimmy's Tapas Bar Website!**