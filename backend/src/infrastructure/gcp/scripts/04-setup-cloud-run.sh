#!/bin/bash
# Setup Cloud Run service

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../configs/project.env"

echo "=== Setting up Cloud Run ==="
echo "Service: ${SERVICE_NAME}"
echo "Region: ${GCP_REGION}"
echo ""

# Create VPC connector for Cloud Run to access VPC resources
CONNECTOR_NAME="codementor-connector"

if gcloud compute networks vpc-access connectors describe "${CONNECTOR_NAME}" \
    --region="${GCP_REGION}" \
    --project="${PROJECT_ID}" &>/dev/null; then
    echo "✓ VPC connector already exists"
else
    echo "Creating VPC connector..."
    gcloud compute networks vpc-access connectors create "${CONNECTOR_NAME}" \
        --region="${GCP_REGION}" \
        --network="${VPC_NETWORK_NAME}" \
        --range="10.8.0.0/28" \
        --min-instances=2 \
        --max-instances=3 \
        --machine-type=f1-micro \
        --project="${PROJECT_ID}"
    
    echo "✓ VPC connector created"
fi

# Grant Cloud Run service account access to secrets
echo "Granting service account access to secrets..."
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

for SECRET in "database-url" "redis-url" "db-password"; do
    gcloud secrets add-iam-policy-binding "${SECRET}" \
        --member="serviceAccount:${SERVICE_ACCOUNT}" \
        --role="roles/secretmanager.secretAccessor" \
        --project="${PROJECT_ID}" \
        2>/dev/null || true
done

echo "✓ Service account permissions configured"

echo ""
echo "=== Cloud Run Setup Complete ==="
echo "VPC Connector: ${CONNECTOR_NAME}"
echo "Service Account: ${SERVICE_ACCOUNT}"
echo ""
echo "To deploy the application:"
echo "1. Build the Docker image: gcloud builds submit --tag gcr.io/${PROJECT_ID}/codementor-backend"
echo "2. Deploy to Cloud Run: gcloud run deploy ${SERVICE_NAME} --image gcr.io/${PROJECT_ID}/codementor-backend ..."
echo ""
echo "Next step: Run ./05-setup-ci-cd.sh"
