FROM python:3.11-slim-bookworm

# Install system dependencies
# Odoo requires:
# - build-essential, python3-dev (for compiling python packages)
# - libldap2-dev, libsasl2-dev (for python-ldap)
# - libpq-dev (for psycopg2)
# - libjpeg-dev, zlib1g-dev (for Pillow)
# - libxml2-dev, libxslt1-dev (for lxml)
# - nodejs, npm (for web assets - optional but good for static assets if needed, though strictly python deps are critical)
# - rtlcss (for RTL support, if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libldap2-dev \
    libsasl2-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install rtlcss for RTL support
RUN npm install -g rtlcss

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Odoo port
EXPOSE 8069

# Set default environment variables
ENV ODOO_RC /etc/odoo/odoo.conf
ENV ODOO_DATA_DIR /var/lib/odoo

# Create a placeholder config file if not passed via env vars, 
# but we expect RAILWAY to inject env vars or we use a custom entrypoint.
# For simplicity, we'll run odoo-bin directly. 
# Railway provides PORT env var, but Odoo expects http_port.
# We can use a small shell script as entrypoint to map PORT to --http-port if needed, 
# or just assume user sets ODOO_HTTP_PORT/HTTP_PORT env var if convenient, 
# but Odoo uses `http_port` in config or `--http-port` CLI arg.

# Create a simple entrypoint script to handle configuration
RUN echo '#!/bin/bash' > /app/entrypoint.sh && \
    echo 'if [ -z "$PORT" ]; then PORT=8069; fi' >> /app/entrypoint.sh && \
    echo 'exec python3 odoo-bin --http-port=$PORT --no-database-list "$@"' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

USER 1000:1000

CMD ["/app/entrypoint.sh"]
