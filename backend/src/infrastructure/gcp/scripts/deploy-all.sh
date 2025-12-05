#!/bin/bash
# Master deployment script for CodeMentor GCP infrastructure
# Runs all setup scripts in sequence

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   CodeMentor GCP Infrastructure Deployment                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if configuration exists
if [ ! -f "${SCRIPT_DIR}/../configs/project.env" ]; then
    echo "❌ Error: Configuration file not found!"
    echo "Please configure infrastructure/gcp/configs/project.env first"
    exit 1
fi

# Load configuration
source "${SCRIPT_DIR}/../configs/project.env"

echo "Configuration:"
echo "  Project ID: ${PROJECT_ID}"
echo "  Region: ${GCP_REGION}"
echo "  Environment: ${ENVIRONMENT}"
echo ""

read -p "Deploy infrastructure with these settings? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

echo ""
echo "Starting deployment..."
echo ""

# Step 1: Project setup
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1/6: Project Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bash "${SCRIPT_DIR}/00-setup-project.sh"

# Step 2: Network setup
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2/6: Network Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bash "${SCRIPT_DIR}/01-setup-network.sh"

# Step 3: Database provisioning
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3/6: Database Provisioning"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bash "${SCRIPT_DIR}/02-provision-database.sh"

# Step 4: Redis provisioning
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4/6: Redis Provisioning"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bash "${SCRIPT_DIR}/03-provision-redis.sh"

# Step 5: Cloud Run setup
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5/6: Cloud Run Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bash "${SCRIPT_DIR}/04-setup-cloud-run.sh"

# Step 6: CI/CD setup
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6/6: CI/CD Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bash "${SCRIPT_DIR}/05-setup-ci-cd.sh"

# Step 7: Monitoring setup
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Bonus: Monitoring Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bash "${SCRIPT_DIR}/06-setup-monitoring.sh"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Infrastructure Deployment Complete!                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Build and deploy the application:"
echo "   cd backend && gcloud builds submit --config=../infrastructure/gcp/cloudbuild.yaml"
echo ""
echo "2. Get service URL:"
echo "   gcloud run services describe codementor-backend --region=${GCP_REGION} --format='value(status.url)'"
echo ""
echo "3. View logs:"
echo "   gcloud logging read 'resource.type=\"cloud_run_revision\"' --limit=50"
echo ""
echo "4. View in Console:"
echo "   https://console.cloud.google.com/run?project=${PROJECT_ID}"
echo ""
