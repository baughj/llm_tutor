# CodeMentor GCP Infrastructure

This directory contains infrastructure-as-code for deploying the CodeMentor LLM Coding Tutor Platform on Google Cloud Platform.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Cloud Run (Backend)                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Quart Application (Python)                          │  │
│  │  - API endpoints                                     │  │
│  │  - LLM integration                                   │  │
│  │  - Authentication                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▼
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
  ┌─────────────────┐            ┌──────────────────┐
  │  Cloud SQL      │            │   Memorystore    │
  │  (PostgreSQL)   │            │   (Redis)        │
  │                 │            │                  │
  │  - User data    │            │  - Sessions      │
  │  - Exercises    │            │  - Cache         │
  │  - Progress     │            │  - Rate limiting │
  └─────────────────┘            └──────────────────┘
```

## Prerequisites

1. **Google Cloud SDK** installed and configured
   ```bash
   gcloud version
   gcloud auth login
   ```

2. **Billing Account** with sufficient quota
   - Cloud SQL instances
   - Memorystore instances
   - Cloud Run services

3. **Required permissions**
   - Project Creator (if creating new project)
   - Editor or Owner on the project
   - Billing Account User

## Quick Start

### 1. Configure Project Settings

Edit `configs/project.env` with your project settings:

```bash
export PROJECT_ID="your-project-id"
export BILLING_ACCOUNT_ID="your-billing-account-id"
# ... other settings
```

### 2. Deploy All Infrastructure

Run the master deployment script:

```bash
cd infrastructure/gcp/scripts
./deploy-all.sh
```

This will sequentially execute:
- Project setup and API enablement
- VPC network creation
- Cloud SQL PostgreSQL provisioning
- Memorystore Redis provisioning
- Cloud Run configuration
- CI/CD pipeline setup
- Monitoring and logging configuration

### 3. Deploy Application

After infrastructure is ready:

```bash
cd backend
gcloud builds submit --config=../infrastructure/gcp/cloudbuild.yaml
```

## Manual Step-by-Step Deployment

If you prefer to deploy components individually:

```bash
cd infrastructure/gcp/scripts

# Step 1: Setup project and enable APIs
./00-setup-project.sh

# Step 2: Create VPC network
./01-setup-network.sh

# Step 3: Provision Cloud SQL (PostgreSQL)
./02-provision-database.sh

# Step 4: Provision Memorystore (Redis)
./03-provision-redis.sh

# Step 5: Setup Cloud Run
./04-setup-cloud-run.sh

# Step 6: Configure CI/CD
./05-setup-ci-cd.sh

# Step 7: Setup monitoring
./06-setup-monitoring.sh
```

## Resource Details

### Cloud SQL (PostgreSQL)
- **Instance Type**: db-f1-micro (dev) / db-custom-2-7680 (prod)
- **Version**: PostgreSQL 15
- **Networking**: Private IP only (within VPC)
- **Backups**: Daily at 3:00 AM UTC
- **High Availability**: Available for production

### Memorystore (Redis)
- **Tier**: Basic (dev) / Standard HA (prod)
- **Memory**: 1GB (minimum)
- **Version**: Redis 7.0
- **Networking**: Within VPC only

### Cloud Run
- **Concurrency**: 80 requests per instance
- **Memory**: 512Mi
- **CPU**: 1
- **Scaling**: 0-10 instances (autoscaling)
- **Timeout**: 300 seconds
- **VPC Access**: Via VPC Connector

### Networking
- **VPC**: Custom VPC network
- **Subnet**: us-central1, /20 CIDR
- **VPC Connector**: f1-micro, 2-3 instances
- **Firewall**: Internal traffic + SSH

## Secrets Management

Sensitive data is stored in **Secret Manager**:

- `database-url`: PostgreSQL connection string
- `db-password`: Database user password
- `redis-url`: Redis connection string

Access secrets:
```bash
gcloud secrets versions access latest --secret="database-url"
```

## Monitoring and Logging

### View Logs
```bash
# Cloud Run logs
gcloud logging read 'resource.type="cloud_run_revision"' --limit=50

# Database logs
gcloud logging read 'resource.type="cloudsql_database"' --limit=50
```

### Metrics Dashboard
Access in Cloud Console:
```
https://console.cloud.google.com/monitoring?project=YOUR_PROJECT_ID
```

### Alerts
Configured alerts:
- High error rate (>5% 5xx responses)
- Service availability
- Database connection issues

## Cost Estimation

**Development Environment** (~$50-100/month):
- Cloud SQL (db-f1-micro): ~$15/month
- Memorystore (1GB Basic): ~$30/month
- Cloud Run (minimal traffic): ~$5-20/month
- Networking: ~$5/month
- Logging/Monitoring: ~$5/month

**Production Environment** (~$200-500/month):
- Cloud SQL (db-custom-2-7680): ~$100/month
- Memorystore (5GB Standard HA): ~$150/month
- Cloud Run (moderate traffic): ~$50-150/month
- Networking: ~$20/month
- Logging/Monitoring: ~$20/month

## Cleanup

To delete all resources:

```bash
# Delete Cloud Run service
gcloud run services delete codementor-backend --region=us-central1

# Delete Cloud SQL instance
gcloud sql instances delete codementor-db

# Delete Redis instance
gcloud redis instances delete codementor-cache --region=us-central1

# Delete VPC connector
gcloud compute networks vpc-access connectors delete codementor-connector --region=us-central1

# Delete VPC network
gcloud compute networks delete codementor-vpc

# Delete project (careful!)
gcloud projects delete YOUR_PROJECT_ID
```

## Troubleshooting

### Common Issues

**1. "Insufficient quota" errors**
- Request quota increase in Cloud Console
- Use smaller instance types for development

**2. VPC peering issues**
- Ensure servicenetworking API is enabled
- Check IP range reservation

**3. Cloud Run cannot connect to Cloud SQL**
- Verify VPC connector is created
- Check firewall rules
- Verify service account permissions

**4. Secrets not accessible**
- Grant Secret Manager access to Cloud Run service account
- Check secret names match configuration

## Support

For issues or questions:
1. Check logs: `gcloud logging read`
2. Verify configuration in `configs/project.env`
3. Review GCP Console for resource status
4. Contact DevOps team

## Security Considerations

- ✅ Database uses private IP only (no public access)
- ✅ Redis uses private IP only
- ✅ Secrets stored in Secret Manager
- ✅ TLS/SSL enabled for all services
- ✅ VPC network isolation
- ✅ Service account with least privilege
- ⚠️ Review and update firewall rules regularly
- ⚠️ Enable Cloud Armor for DDoS protection (production)
- ⚠️ Implement Identity-Aware Proxy for admin access

## License

Internal - All Rights Reserved
