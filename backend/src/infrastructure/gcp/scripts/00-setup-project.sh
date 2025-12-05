#!/bin/bash
# Setup GCP project and enable required APIs

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../configs/project.env"

echo "=== CodeMentor GCP Project Setup ==="
echo "Project ID: ${PROJECT_ID}"
echo "Region: ${GCP_REGION}"
echo ""

# Create project (if it doesn't exist)
if gcloud projects describe "${PROJECT_ID}" &>/dev/null; then
    echo "✓ Project ${PROJECT_ID} already exists"
else
    echo "Creating project ${PROJECT_ID}..."
    if [ -n "${ORGANIZATION_ID}" ]; then
        gcloud projects create "${PROJECT_ID}" \
            --name="${PROJECT_NAME}" \
            --organization="${ORGANIZATION_ID}"
    else
        gcloud projects create "${PROJECT_ID}" \
            --name="${PROJECT_NAME}"
    fi
    echo "✓ Project created"
fi

# Set active project
gcloud config set project "${PROJECT_ID}"
echo "✓ Active project set to ${PROJECT_ID}"

# Link billing account
if [ -n "${BILLING_ACCOUNT_ID}" ]; then
    echo "Linking billing account..."
    gcloud beta billing projects link "${PROJECT_ID}" \
        --billing-account="${BILLING_ACCOUNT_ID}"
    echo "✓ Billing account linked"
else
    echo "⚠ BILLING_ACCOUNT_ID not set. Please link billing manually."
fi

# Enable required APIs
echo "Enabling required GCP APIs..."
gcloud services enable \
    compute.googleapis.com \
    servicenetworking.googleapis.com \
    sqladmin.googleapis.com \
    redis.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com \
    cloudresourcemanager.googleapis.com \
    logging.googleapis.com \
    monitoring.googleapis.com \
    cloudtrace.googleapis.com \
    --project="${PROJECT_ID}"

echo "✓ All APIs enabled"

# Set default region and zone
gcloud config set compute/region "${GCP_REGION}"
gcloud config set compute/zone "${GCP_ZONE}"
echo "✓ Default region and zone configured"

echo ""
echo "=== Project Setup Complete ==="
echo "Project ID: ${PROJECT_ID}"
echo "Region: ${GCP_REGION}"
echo "Zone: ${GCP_ZONE}"
echo ""
echo "Next steps:"
echo "1. Run: ./01-setup-network.sh"
echo "2. Run: ./02-provision-database.sh"
echo "3. Run: ./03-provision-redis.sh"
