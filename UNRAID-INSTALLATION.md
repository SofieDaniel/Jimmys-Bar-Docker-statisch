# Jimmy's Tapas Bar - Docker Deployment

## 🐳 Für Unraid Installation

### Schnell-Installation:

1. **Unraid App hinzufügen:**
   - Gehe zu "Docker" Tab in Unraid
   - Klicke "Add Container"
   - Verwende diese Einstellungen:

**Container Einstellungen:**
```
Name: jimmys-tapas-bar
Repository: jimmys-tapas:latest
Network Type: Bridge
Console Shell: Bash

Port Mappings:
- Container Port: 80 -> Host Port: 80 (Website)
- Container Port: 8001 -> Host Port: 8001 (API)

Volume Mappings:
- Container Path: /var/lib/mysql -> Host Path: /mnt/user/appdata/jimmys-tapas/mysql
- Container Path: /app/backups -> Host Path: /mnt/user/appdata/jimmys-tapas/backups

Environment Variables:
- MYSQL_ROOT_PASSWORD=jimmy2024
- MYSQL_DATABASE=jimmys_tapas_bar
- JWT_SECRET_KEY=jimmy-tapas-bar-mysql-secret-2024
```

### 🔧 Admin-Zugang:
- **URL:** `http://IHR-UNRAID-IP/admin`
- **Username:** `admin`
- **Passwort:** `jimmy2024`

### 📋 Funktionen:
✅ **Speisekarte:** 141 Artikel mit MouseOver-Details  
✅ **CMS:** Vollständige Bearbeitung aller Inhalte  
✅ **Kontaktformular:** Funktional mit E-Mail-Sammlung  
✅ **Standorte:** Editierbare Standort-Informationen  
✅ **Benutzer-Verwaltung:** Admin-Panel  
✅ **EU-Compliance:** DSGVO & Cookie-Management  
✅ **Auto-Backup:** MySQL-Backups im CMS  

### 🚀 Installation via Docker Compose:

1. **Dateien hochladen** auf Unraid:
   ```bash
   # Alle Dateien in /mnt/user/appdata/jimmys-tapas/
   ```

2. **Container builden:**
   ```bash
   cd /mnt/user/appdata/jimmys-tapas/
   docker-compose up -d
   ```

### 🌐 Nach Installation:
- **Website:** `http://IHR-UNRAID-IP`
- **Admin-Panel:** `http://IHR-UNRAID-IP/admin`

### 📊 Health Check:
Der Container prüft automatisch die Gesundheit und startet bei Problemen neu.

### 💾 Daten-Persistierung:
- MySQL-Daten in `/mnt/user/appdata/jimmys-tapas/mysql`
- Backups in `/mnt/user/appdata/jimmys-tapas/backups`

### 🔄 Updates:
```bash
docker-compose pull
docker-compose up -d
```