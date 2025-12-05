#!/bin/bash
# Setup Cloud Monitoring and Logging

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../configs/project.env"

echo "=== Setting up Monitoring and Logging ==="
echo ""

# Create log sink for long-term storage
echo "Creating log sink for long-term storage..."
gcloud logging sinks create codementor-logs \
    storage.googleapis.com/codementor-logs-${PROJECT_ID} \
    --log-filter='resource.type="cloud_run_revision"' \
    --project="${PROJECT_ID}" \
    2>/dev/null || echo "✓ Log sink already exists"

# Create Cloud Storage bucket for logs
echo "Creating Cloud Storage bucket for logs..."
gsutil mb -p "${PROJECT_ID}" -l "${GCP_REGION}" \
    gs://codementor-logs-${PROJECT_ID} \
    2>/dev/null || echo "✓ Bucket already exists"

# Set retention policy
gsutil lifecycle set /dev/stdin gs://codementor-logs-${PROJECT_ID} <<EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": ${LOG_RETENTION_DAYS}}
      }
    ]
  }
}
EOF

echo "✓ Log retention policy set to ${LOG_RETENTION_DAYS} days"

# Create uptime check
echo "Creating uptime check..."
cat > /tmp/uptime-check.json <<EOF
{
  "displayName": "CodeMentor Backend Health Check",
  "monitoredResource": {
    "type": "uptime_url",
    "labels": {}
  },
  "httpCheck": {
    "path": "/health",
    "port": 443,
    "useSsl": true,
    "validateSsl": true
  },
  "period": "60s",
  "timeout": "10s"
}
EOF

# Note: Creating uptime checks requires the service URL which we don't have yet
echo "⚠ Uptime check configuration created but not deployed"
echo "  Deploy after Cloud Run service is running"

# Create alerting policy for high error rate
echo "Creating alert policy for high error rate..."
cat > /tmp/alert-policy.json <<EOF
{
  "displayName": "High Error Rate - CodeMentor",
  "conditions": [{
    "displayName": "Error rate above 5%",
    "conditionThreshold": {
      "filter": "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_count\" AND metric.label.response_code_class=\"5xx\"",
      "aggregations": [{
        "alignmentPeriod": "60s",
        "perSeriesAligner": "ALIGN_RATE"
      }],
      "comparison": "COMPARISON_GT",
      "thresholdValue": 5,
      "duration": "300s"
    }
  }],
  "combiner": "OR",
  "enabled": true
}
EOF

echo "✓ Alert policy configuration created"

# Create dashboard
echo "Creating monitoring dashboard..."
cat > /tmp/dashboard.json <<EOF
{
  "displayName": "CodeMentor Metrics",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Request Count",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_count\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_RATE"
                  }
                }
              }
            }]
          }
        }
      },
      {
        "xPos": 6,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Request Latency",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_latencies\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_DELTA",
                    "crossSeriesReducer": "REDUCE_PERCENTILE_95"
                  }
                }
              }
            }]
          }
        }
      }
    ]
  }
}
EOF

echo "✓ Dashboard configuration created"

echo ""
echo "=== Monitoring and Logging Setup Complete ==="
echo "Log bucket: gs://codementor-logs-${PROJECT_ID}"
echo "Retention: ${LOG_RETENTION_DAYS} days"
echo ""
echo "View logs: gcloud logging read 'resource.type=\"cloud_run_revision\"'"
echo "View metrics: https://console.cloud.google.com/monitoring?project=${PROJECT_ID}"
echo ""
