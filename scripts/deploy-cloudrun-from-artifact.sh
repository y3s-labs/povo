#!/bin/bash
set -e

# Configuration - UPDATE THESE VALUES
PROJECT_ID="povo-demo"  # Replace with your GCP project ID
REGION="us-central1"  # Change to your preferred region
REPOSITORY="povo"  # Artifact Registry repository name
IMAGE_NAME="povo-server"
TAG="latest"
SERVICE_NAME="povo-server"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}☁️  Deploying to Cloud Run from Artifact Registry...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo -e "${YELLOW}🔐 Please authenticate with Google Cloud:${NC}"
    gcloud auth login
fi

# Set the project
echo -e "${YELLOW}🎯 Setting project to: $PROJECT_ID${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com

# Construct the full image name
FULL_IMAGE_NAME="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$TAG"

# Check if .env file exists for environment variables
ENV_VARS="ENV=production"
if [[ -f ".env" ]]; then
    echo -e "${YELLOW}📋 Found .env file. Adding environment variables...${NC}"
    # Read .env file and convert to format suitable for gcloud
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip empty lines and comments
        if [[ -n "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
            # Remove any leading/trailing whitespace
            line=$(echo "$line" | xargs)
            if [[ -n "$line" ]]; then
                ENV_VARS="$ENV_VARS,$line"
            fi
        fi
    done < .env
fi

# Deploy to Cloud Run
echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"
echo -e "${YELLOW}Image: $FULL_IMAGE_NAME${NC}"
echo -e "${YELLOW}Environment variables: $ENV_VARS${NC}"

gcloud run deploy $SERVICE_NAME \
  --image=$FULL_IMAGE_NAME \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --port=8080 \
  --memory=1Gi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --timeout=300 \
  --set-env-vars="$ENV_VARS"

echo -e "${GREEN}✅ Deployment completed!${NC}"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform=managed --region=$REGION --format='value(status.url)')
echo -e "${GREEN}🌐 Your service is available at: $SERVICE_URL${NC}"

# Test the deployment
echo -e "${YELLOW}🧪 Testing the deployment...${NC}"
if curl -f -s "$SERVICE_URL/health" > /dev/null; then
    echo -e "${GREEN}✅ Health check passed!${NC}"
else
    echo -e "${YELLOW}⚠️  Health check failed or endpoint not available${NC}"
fi

echo -e "${GREEN}🎉 Deployment successful!${NC}"
echo -e "${GREEN}📚 API Documentation: $SERVICE_URL/docs${NC}"
echo -e "${GREEN}🔍 View logs: gcloud run logs read --service=$SERVICE_NAME --region=$REGION${NC}"
