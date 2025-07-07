#!/bin/bash

echo "🐳 Building Jimmy's Tapas Bar Docker Container..."

# Build the Docker image
docker build -t jimmys-tapas:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "🚀 To run the container:"
    echo "docker run -d -p 80:80 -p 8001:8001 --name jimmys-tapas jimmys-tapas:latest"
    echo ""
    echo "📱 Or use docker-compose:"
    echo "docker-compose up -d"
    echo ""
    echo "🌐 Website will be available at: http://localhost"
    echo "🎛️ Admin panel at: http://localhost/admin"
    echo "👤 Login: admin / jimmy2024"
    echo ""
    echo "📦 To export for Unraid:"
    echo "docker save jimmys-tapas:latest | gzip > jimmys-tapas-unraid.tar.gz"
else
    echo "❌ Docker build failed!"
    exit 1
fi