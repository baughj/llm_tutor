#!/bin/bash
# Setup Cloud Build CI/CD pipeline

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../configs/project.env"

echo "=== Setting up Cloud Build CI/CD ==="
echo ""

# Grant Cloud Build service account necessary permissions
echo "Configuring Cloud Build service account permissions..."
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")
CLOUDBUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

# Grant permissions
for ROLE in "roles/run.admin" "roles/iam.serviceAccountUser" "roles/secretmanager.secretAccessor"; do
    gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
        --member="serviceAccount:${CLOUDBUILD_SA}" \
        --role="${ROLE}" \
        --condition=None \
        2>/dev/null || true
done

echo "✓ Cloud Build service account permissions configured"

# Create build trigger (requires GitHub connection)
echo ""
echo "To create a build trigger:"
echo "1. Connect your GitHub repository:"
echo "   gcloud builds triggers create github \\"
echo "     --repo-name=${REPO_NAME} \\"
echo "     --repo-owner=<YOUR_GITHUB_USERNAME> \\"
echo "     --branch-pattern=\"^${BRANCH_NAME}\$\" \\"
echo "     --build-config=infrastructure/gcp/cloudbuild.yaml"
echo ""
echo "2. Or manually trigger a build:"
echo "   gcloud builds submit --config=infrastructure/gcp/cloudbuild.yaml"
echo ""

echo "=== CI/CD Setup Complete ==="
echo "Build configuration: infrastructure/gcp/cloudbuild.yaml"
echo ""
echo "Next step: Run ./06-setup-monitoring.sh"
