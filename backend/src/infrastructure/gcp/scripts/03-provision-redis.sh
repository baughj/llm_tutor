#!/bin/bash
# Provision Memorystore Redis instance

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../configs/project.env"

echo "=== Provisioning Memorystore Redis ==="
echo "Instance: ${REDIS_INSTANCE_NAME}"
echo "Tier: ${REDIS_TIER}"
echo "Memory: ${REDIS_MEMORY_SIZE_GB}GB"
echo ""

# Check if instance already exists
if gcloud redis instances describe "${REDIS_INSTANCE_NAME}" \
    --region="${GCP_REGION}" \
    --project="${PROJECT_ID}" &>/dev/null; then
    echo "✓ Redis instance ${REDIS_INSTANCE_NAME} already exists"
else
    echo "Creating Redis instance (this may take several minutes)..."
    gcloud redis instances create "${REDIS_INSTANCE_NAME}" \
        --size="${REDIS_MEMORY_SIZE_GB}" \
        --region="${GCP_REGION}" \
        --redis-version="${REDIS_VERSION}" \
        --tier="${REDIS_TIER}" \
        --network="projects/${PROJECT_ID}/global/networks/${VPC_NETWORK_NAME}" \
        --project="${PROJECT_ID}"
    
    echo "✓ Redis instance created"
fi

# Get connection info
REDIS_HOST=$(gcloud redis instances describe "${REDIS_INSTANCE_NAME}" \
    --region="${GCP_REGION}" \
    --project="${PROJECT_ID}" \
    --format="value(host)")

REDIS_PORT=$(gcloud redis instances describe "${REDIS_INSTANCE_NAME}" \
    --region="${GCP_REGION}" \
    --project="${PROJECT_ID}" \
    --format="value(port)")

# Create Redis URL secret
echo "Storing Redis connection string in Secret Manager..."
REDIS_URL="redis://${REDIS_HOST}:${REDIS_PORT}/0"
REDIS_URL_SECRET="redis-url"

if gcloud secrets describe "${REDIS_URL_SECRET}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "Updating Redis URL secret..."
    echo -n "${REDIS_URL}" | gcloud secrets versions add "${REDIS_URL_SECRET}" \
        --data-file=- \
        --project="${PROJECT_ID}"
else
    echo -n "${REDIS_URL}" | gcloud secrets create "${REDIS_URL_SECRET}" \
        --data-file=- \
        --replication-policy="automatic" \
        --project="${PROJECT_ID}"
fi

echo "✓ Redis URL stored in Secret Manager"

echo ""
echo "=== Redis Setup Complete ==="
echo "Instance: ${REDIS_INSTANCE_NAME}"
echo "Host: ${REDIS_HOST}"
echo "Port: ${REDIS_PORT}"
echo ""
echo "Connection string stored in Secret Manager: ${REDIS_URL_SECRET}"
echo ""
echo "Next step: Run ./04-setup-cloud-run.sh"
