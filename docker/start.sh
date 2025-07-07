#!/bin/bash
set -e

echo "🚀 Starting Jimmy's Tapas Bar Docker Container..."

# Initialize MySQL
echo "📊 Initializing MySQL..."
mysql_install_db --user=mysql --datadir=/var/lib/mysql --rpm

# Start MySQL in background
mysqld_safe --user=mysql &
sleep 10

# Initialize database
echo "🗃️ Setting up database..."
mysql < /docker-entrypoint-initdb.d/init-mysql.sql

# Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to be ready..."
until mysqladmin ping --silent; do
    echo "Waiting for MySQL..."
    sleep 2
done

echo "✅ MySQL is ready!"

# Import full menu data if available
if [ -f "/app/backend/import_complete_menu_final.py" ]; then
    echo "📋 Importing menu data..."
    cd /app/backend
    python import_complete_menu_final.py || echo "Menu import skipped"
fi

echo "🎯 Starting all services with Supervisor..."

# Start supervisor (manages all services: MySQL, Backend, Nginx)
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf