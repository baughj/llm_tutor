#!/bin/bash
# Setup VPC network and configure networking

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../configs/project.env"

echo "=== Setting up VPC Network ==="
echo "Network: ${VPC_NETWORK_NAME}"
echo "Subnet: ${SUBNET_NAME} (${SUBNET_RANGE})"
echo ""

# Create VPC network
if gcloud compute networks describe "${VPC_NETWORK_NAME}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "✓ VPC network ${VPC_NETWORK_NAME} already exists"
else
    echo "Creating VPC network..."
    gcloud compute networks create "${VPC_NETWORK_NAME}" \
        --subnet-mode=custom \
        --bgp-routing-mode=regional \
        --project="${PROJECT_ID}"
    echo "✓ VPC network created"
fi

# Create subnet
if gcloud compute networks subnets describe "${SUBNET_NAME}" --region="${GCP_REGION}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "✓ Subnet ${SUBNET_NAME} already exists"
else
    echo "Creating subnet..."
    gcloud compute networks subnets create "${SUBNET_NAME}" \
        --network="${VPC_NETWORK_NAME}" \
        --region="${GCP_REGION}" \
        --range="${SUBNET_RANGE}" \
        --enable-private-ip-google-access \
        --project="${PROJECT_ID}"
    echo "✓ Subnet created"
fi

# Create firewall rules
echo "Creating firewall rules..."

# Allow internal communication
gcloud compute firewall-rules create "${VPC_NETWORK_NAME}-allow-internal" \
    --network="${VPC_NETWORK_NAME}" \
    --allow=tcp:0-65535,udp:0-65535,icmp \
    --source-ranges="${SUBNET_RANGE}" \
    --project="${PROJECT_ID}" \
    --description="Allow internal communication within VPC" \
    2>/dev/null || echo "✓ Internal firewall rule already exists"

# Allow SSH (for debugging)
gcloud compute firewall-rules create "${VPC_NETWORK_NAME}-allow-ssh" \
    --network="${VPC_NETWORK_NAME}" \
    --allow=tcp:22 \
    --source-ranges=0.0.0.0/0 \
    --project="${PROJECT_ID}" \
    --description="Allow SSH access" \
    2>/dev/null || echo "✓ SSH firewall rule already exists"

# Reserve IP range for VPC peering (needed for Cloud SQL)
echo "Reserving IP range for VPC peering..."
gcloud compute addresses create google-managed-services-"${VPC_NETWORK_NAME}" \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=16 \
    --network="${VPC_NETWORK_NAME}" \
    --project="${PROJECT_ID}" \
    2>/dev/null || echo "✓ IP range already reserved"

# Create VPC peering connection (for Cloud SQL private IP)
echo "Creating VPC peering connection..."
gcloud services vpc-peerings connect \
    --service=servicenetworking.googleapis.com \
    --ranges=google-managed-services-"${VPC_NETWORK_NAME}" \
    --network="${VPC_NETWORK_NAME}" \
    --project="${PROJECT_ID}" \
    2>/dev/null || echo "✓ VPC peering already configured"

echo ""
echo "=== Network Setup Complete ==="
echo "VPC Network: ${VPC_NETWORK_NAME}"
echo "Subnet: ${SUBNET_NAME}"
echo ""
echo "Next step: Run ./02-provision-database.sh"
