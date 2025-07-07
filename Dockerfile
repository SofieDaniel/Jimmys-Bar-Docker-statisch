FROM node:18-alpine as frontend-builder

# Install dependencies
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install

# Copy source and build
COPY frontend/ ./
RUN npm run build

# Python backend with MySQL
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    mariadb-server \
    mariadb-client \
    nginx \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy backend requirements and install
COPY backend/requirements.txt ./backend/
RUN pip install -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy MySQL initialization script
COPY docker/init-mysql.sql /docker-entrypoint-initdb.d/

# Create necessary directories
RUN mkdir -p /var/log/supervisor /app/backups /run/mysqld

# Set permissions
RUN chown -R mysql:mysql /var/lib/mysql /run/mysqld

# Expose ports
EXPOSE 80 8001

# Copy startup script
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80 || exit 1

CMD ["/start.sh"]
