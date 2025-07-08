#!/bin/bash

# 🐳 JIMMY'S TAPAS BAR - UNRAID QUICK SETUP SCRIPT
# Dieses Script automatisiert die Installation auf Unraid

echo "🌶️ Jimmy's Tapas Bar - Unraid Setup wird gestartet..."

# Farben für bessere Lesbarkeit
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Prüfen ob Docker installiert ist
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker ist nicht installiert!${NC}"
    echo "Bitte installieren Sie Docker auf Ihrem Unraid System."
    exit 1
fi

echo -e "${GREEN}✅ Docker gefunden${NC}"

# Aktuelles Verzeichnis prüfen
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}❌ Dockerfile nicht gefunden!${NC}"
    echo "Bitte führen Sie dieses Script im jimmys-tapas-bar Verzeichnis aus."
    exit 1
fi

echo -e "${GREEN}✅ Dockerfile gefunden${NC}"

# Prüfen ob alle notwendigen Dateien vorhanden sind
required_files=("index.html" "css/styles.css" "js/main.js" "config/menu.ini")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Datei fehlt: $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Alle notwendigen Dateien vorhanden${NC}"

# Alten Container stoppen und entfernen (falls vorhanden)
if docker ps -a | grep -q jimmys-tapas-bar; then
    echo -e "${YELLOW}⚠️ Stoppe alten Container...${NC}"
    docker stop jimmys-tapas-bar 2>/dev/null
    docker rm jimmys-tapas-bar 2>/dev/null
fi

# Altes Image entfernen (falls vorhanden)
if docker images | grep -q jimmys-tapas-bar; then
    echo -e "${YELLOW}⚠️ Entferne altes Image...${NC}"
    docker rmi jimmys-tapas-bar:latest 2>/dev/null
fi

# Docker Image erstellen
echo -e "${BLUE}🔨 Erstelle Docker Image...${NC}"
if docker build -t jimmys-tapas-bar:latest .; then
    echo -e "${GREEN}✅ Docker Image erfolgreich erstellt${NC}"
else
    echo -e "${RED}❌ Fehler beim Erstellen des Docker Images${NC}"
    exit 1
fi

# Port prüfen und Container starten
PORT=8080
while netstat -tuln | grep -q ":$PORT "; do
    echo -e "${YELLOW}⚠️ Port $PORT ist bereits belegt, versuche Port $((++PORT))${NC}"
done

echo -e "${BLUE}🚀 Starte Container auf Port $PORT...${NC}"

# Container starten
if docker run -d \
    --name jimmys-tapas-bar \
    --restart unless-stopped \
    -p $PORT:80 \
    -v "$(pwd):/usr/share/nginx/html:ro" \
    jimmys-tapas-bar:latest; then
    
    echo -e "${GREEN}🎉 Container erfolgreich gestartet!${NC}"
    echo ""
    echo "🌐 Website ist verfügbar unter:"
    echo -e "${BLUE}   http://$(hostname -I | awk '{print $1}'):$PORT${NC}"
    echo ""
    echo "📋 Container-Informationen:"
    echo -e "${BLUE}   Name: jimmys-tapas-bar${NC}"
    echo -e "${BLUE}   Port: $PORT${NC}"
    echo -e "${BLUE}   Status: $(docker ps --format 'table {{.Status}}' --filter name=jimmys-tapas-bar | tail -n 1)${NC}"
    echo ""
    echo "🛠️ Nützliche Befehle:"
    echo "   Container stoppen:    docker stop jimmys-tapas-bar"
    echo "   Container starten:    docker start jimmys-tapas-bar"
    echo "   Logs anzeigen:        docker logs jimmys-tapas-bar"
    echo "   Container entfernen:  docker rm jimmys-tapas-bar"
    
else
    echo -e "${RED}❌ Fehler beim Starten des Containers${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Setup abgeschlossen! Viel Spaß mit Jimmy's Tapas Bar!${NC}"