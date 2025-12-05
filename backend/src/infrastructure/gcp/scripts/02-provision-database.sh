#!/bin/bash
# Provision Cloud SQL PostgreSQL instance

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../configs/project.env"

echo "=== Provisioning Cloud SQL PostgreSQL ==="
echo "Instance: ${DB_INSTANCE_NAME}"
echo "Version: ${DB_VERSION}"
echo "Tier: ${DB_TIER}"
echo ""

# Check if instance already exists
if gcloud sql instances describe "${DB_INSTANCE_NAME}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "✓ Cloud SQL instance ${DB_INSTANCE_NAME} already exists"
else
    echo "Creating Cloud SQL instance (this may take several minutes)..."
    gcloud sql instances create "${DB_INSTANCE_NAME}" \
        --database-version="${DB_VERSION}" \
        --tier="${DB_TIER}" \
        --region="${GCP_REGION}" \
        --network="projects/${PROJECT_ID}/global/networks/${VPC_NETWORK_NAME}" \
        --no-assign-ip \
        --enable-google-private-path \
        --backup-start-time="03:00" \
        --database-flags=max_connections=100 \
        --maintenance-window-day=SUN \
        --maintenance-window-hour=4 \
        --project="${PROJECT_ID}"
    
    echo "✓ Cloud SQL instance created"
fi

# Generate database password if not exists in Secret Manager
echo "Setting up database password in Secret Manager..."
DB_PASSWORD_SECRET="db-password"

if gcloud secrets describe "${DB_PASSWORD_SECRET}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "✓ Database password secret already exists"
    DB_PASSWORD=$(gcloud secrets versions access latest --secret="${DB_PASSWORD_SECRET}" --project="${PROJECT_ID}")
else
    # Generate secure random password
    DB_PASSWORD=$(openssl rand -base64 32)
    echo -n "${DB_PASSWORD}" | gcloud secrets create "${DB_PASSWORD_SECRET}" \
        --data-file=- \
        --replication-policy="automatic" \
        --project="${PROJECT_ID}"
    echo "✓ Database password created and stored in Secret Manager"
fi

# Create database
echo "Creating database ${DB_NAME}..."
gcloud sql databases create "${DB_NAME}" \
    --instance="${DB_INSTANCE_NAME}" \
    --project="${PROJECT_ID}" \
    2>/dev/null || echo "✓ Database already exists"

# Create database user
echo "Creating database user..."
gcloud sql users create "${DB_USER}" \
    --instance="${DB_INSTANCE_NAME}" \
    --password="${DB_PASSWORD}" \
    --project="${PROJECT_ID}" \
    2>/dev/null || echo "✓ Database user already exists"

# Get connection info
CONNECTION_NAME=$(gcloud sql instances describe "${DB_INSTANCE_NAME}" \
    --project="${PROJECT_ID}" \
    --format="value(connectionName)")

PRIVATE_IP=$(gcloud sql instances describe "${DB_INSTANCE_NAME}" \
    --project="${PROJECT_ID}" \
    --format="value(ipAddresses[0].ipAddress)")

# Create connection string secret
echo "Storing database connection string in Secret Manager..."
DB_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${PRIVATE_IP}:5432/${DB_NAME}"
DB_URL_SECRET="database-url"

if gcloud secrets describe "${DB_URL_SECRET}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "Updating database URL secret..."
    echo -n "${DB_URL}" | gcloud secrets versions add "${DB_URL_SECRET}" \
        --data-file=- \
        --project="${PROJECT_ID}"
else
    echo -n "${DB_URL}" | gcloud secrets create "${DB_URL_SECRET}" \
        --data-file=- \
        --replication-policy="automatic" \
        --project="${PROJECT_ID}"
fi

echo "✓ Database URL stored in Secret Manager"

echo ""
echo "=== Cloud SQL Setup Complete ==="
echo "Instance: ${DB_INSTANCE_NAME}"
echo "Connection Name: ${CONNECTION_NAME}"
echo "Private IP: ${PRIVATE_IP}"
echo "Database: ${DB_NAME}"
echo "User: ${DB_USER}"
echo ""
echo "Connection string stored in Secret Manager: ${DB_URL_SECRET}"
echo ""
echo "Next step: Run ./03-provision-redis.sh"
