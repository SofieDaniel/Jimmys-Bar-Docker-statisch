# 🐳 UNRAID INSTALLATION ANLEITUNG - JIMMY'S TAPAS BAR WEBSITE

## 📋 SCHRITT-FÜR-SCHRITT INSTALLATION:

### **SCHRITT 1: Repository auf Unraid herunterladen**
```bash
# SSH zu Unraid oder Terminal öffnen
cd /mnt/user/appdata/
git clone [IHR_GIT_REPOSITORY_URL] jimmys-tapas-bar
cd jimmys-tapas-bar
```

### **SCHRITT 2: Docker Image erstellen**
```bash
# Im jimmys-tapas-bar Verzeichnis
docker build -t jimmys-tapas-bar:latest .
```

### **SCHRITT 3: Container in Unraid hinzufügen**

**Option A: Via Unraid WebUI (Empfohlen)**
1. Gehen Sie zu `Apps` → `Docker` → `Add Container`
2. Folgende Einstellungen verwenden:

```
Name: jimmys-tapas-bar
Repository: jimmys-tapas-bar:latest
Network Type: bridge
Console shell command: bash

Port Mappings:
Container Port: 80
Host Port: 8080 (oder gewünschter Port)
Connection Type: TCP

Path Mappings:
Container Path: /usr/share/nginx/html
Host Path: /mnt/user/appdata/jimmys-tapas-bar
Access Mode: Read Only

Extra Parameters: 
--restart=unless-stopped
```

**Option B: Via Docker Compose (Alternative)**
```yaml
version: '3.8'
services:
  jimmys-tapas-bar:
    build: .
    container_name: jimmys-tapas-bar
    ports:
      - "8080:80"
    volumes:
      - /mnt/user/appdata/jimmys-tapas-bar:/usr/share/nginx/html:ro
    restart: unless-stopped
```

### **SCHRITT 4: Container starten**
```bash
# Via CLI
docker run -d \
  --name jimmys-tapas-bar \
  --restart unless-stopped \
  -p 8080:80 \
  -v /mnt/user/appdata/jimmys-tapas-bar:/usr/share/nginx/html:ro \
  jimmys-tapas-bar:latest
```

### **SCHRITT 5: Zugriff testen**
- Website aufrufen: `http://[UNRAID_IP]:8080`
- Beispiel: `http://192.168.1.100:8080`

## 📁 DATEISTRUKTUR ÜBERSICHT:

```
/mnt/user/appdata/jimmys-tapas-bar/
├── Dockerfile                 # Docker-Konfiguration
├── index.html                 # Hauptseite (Startseite)
├── css/                       # Stylesheets
│   ├── styles.css            # Haupt-CSS
│   ├── speisekarte.css       # Speisekarte-Styles
│   ├── bewertungen.css       # Bewertungen-Styles
│   ├── kontakt.css           # Kontakt-Styles
│   └── ...                   # Weitere CSS-Dateien
├── js/                        # JavaScript-Dateien
│   ├── main.js               # Haupt-JavaScript
│   └── speisekarte.js        # Speisekarte-Funktionen
├── images/                    # Alle Bilder (lokal)
│   ├── hero-tapas-background.jpg
│   ├── paella-specialty.jpg
│   ├── serrano-figs-correct.jpg
│   └── ...                   # Weitere Bilder
├── pages/                     # Unterseiten
│   ├── speisekarte.html      # Speisekarte
│   ├── bewertungen.html      # Bewertungen
│   ├── kontakt.html          # Kontakt
│   ├── ueber-uns.html        # Über uns
│   ├── standorte.html        # Standorte
│   └── impressum.html        # Impressum
└── config/                    # Konfiguration
    └── menu.ini              # Speisekarte-Daten (243 Artikel)
```

## 🛠️ ANPASSUNGEN UND WARTUNG:

### **Inhalte ändern:**
- **Speisekarte**: Bearbeiten Sie `/config/menu.ini`
- **Bilder**: Ersetzen Sie Dateien in `/images/`
- **Texte**: Bearbeiten Sie die entsprechenden HTML-Dateien

### **Container neu starten nach Änderungen:**
```bash
docker restart jimmys-tapas-bar
```

### **Updates installieren:**
```bash
cd /mnt/user/appdata/jimmys-tapas-bar
git pull
docker build -t jimmys-tapas-bar:latest .
docker restart jimmys-tapas-bar
```

## 🔧 TROUBLESHOOTING:

### **Container läuft nicht:**
```bash
# Container-Logs prüfen
docker logs jimmys-tapas-bar

# Container Status prüfen
docker ps -a
```

### **Website nicht erreichbar:**
- Firewall-Einstellungen prüfen
- Port-Mapping überprüfen
- Unraid IP-Adresse bestätigen

### **Bilder laden nicht:**
- Pfad-Mappings überprüfen
- Berechtigung prüfen: `chmod -R 755 /mnt/user/appdata/jimmys-tapas-bar`

## 📊 SYSTEM-ANFORDERUNGEN:

- **RAM**: 256MB minimal
- **Storage**: 50MB für Website-Dateien
- **CPU**: Minimal (statische Website)
- **Ports**: 1 verfügbarer Port (z.B. 8080)

## 🌟 FEATURES DER WEBSITE:

✅ **Vollständig statisch** - keine Datenbank erforderlich
✅ **243 Menüpunkte** in 32 Kategorien
✅ **Lokale Bilder** - schnelle Ladezeiten
✅ **Responsive Design** - funktioniert auf allen Geräten
✅ **Kontaktformular** mit mailto-Funktionalität
✅ **Google Bewertungen** Integration
✅ **Professionelles Design** mit authentischen Bildern

## 🎯 NACH DER INSTALLATION:

1. **Website testen**: `http://[UNRAID_IP]:8080`
2. **Alle Seiten durchklicken**: Speisekarte, Kontakt, etc.
3. **Mobile Ansicht testen**: Responsive Design prüfen
4. **Backup erstellen**: Website-Ordner sichern

**🎉 Viel Erfolg mit Ihrer Jimmy's Tapas Bar Website auf Unraid!**