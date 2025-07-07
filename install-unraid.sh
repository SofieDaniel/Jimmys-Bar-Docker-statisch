#!/bin/bash

echo "🚀 Jimmy's Tapas Bar - Docker Deployment für Unraid"
echo "==============================================="

# Prüfe ob Docker verfügbar ist
if ! command -v docker &> /dev/null; then
    echo "❌ Docker ist nicht installiert!"
    echo "Bitte installieren Sie Docker auf Ihrem Unraid-Server."
    exit 1
fi

echo "📦 Entpacke Deployment-Paket..."
tar -xzf jimmys-tapas-deployment.tar.gz
cd jimmys-tapas-bar/

echo "🔨 Baue Docker Image..."
docker build -t jimmys-tapas:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker Image erfolgreich erstellt!"
    
    echo "💾 Exportiere Image für Unraid..."
    docker save jimmys-tapas:latest | gzip > jimmys-tapas-unraid.tar.gz
    
    echo "🎯 Starte Container (Test)..."
    docker run -d \
        --name jimmys-tapas-test \
        -p 8080:80 \
        -p 8001:8001 \
        jimmys-tapas:latest
    
    echo ""
    echo "🎉 Installation abgeschlossen!"
    echo ""
    echo "📁 Dateien erstellt:"
    echo "   - jimmys-tapas-unraid.tar.gz (für Unraid Import)"
    echo "   - Alle Konfigurationsdateien bereit"
    echo ""
    echo "🌐 Test-Zugang:"
    echo "   Website: http://localhost:8080"
    echo "   Admin:   http://localhost:8080/admin"
    echo "   Login:   admin / jimmy2024"
    echo ""
    echo "🔄 Container stoppen:"
    echo "   docker stop jimmys-tapas-test"
    echo "   docker rm jimmys-tapas-test"
    echo ""
    echo "📤 Für Unraid:"
    echo "   1. jimmys-tapas-unraid.tar.gz auf Unraid hochladen"
    echo "   2. Container erstellen mit Repository: jimmys-tapas:latest"
    echo "   3. Ports: 80:80 und 8001:8001"
else
    echo "❌ Docker Build fehlgeschlagen!"
    exit 1
fi