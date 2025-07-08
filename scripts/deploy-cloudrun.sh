#!/bin/bash
set -e

# Configuration - UPDATE THESE VALUES
DOCKER_HUB_USERNAME="marcher357"  # Replace with your Docker Hub username
IMAGE_NAME="povo-server"
TAG="latest"
PROJECT_ID="povo-demo"  # Replace with your GCP project ID
SERVICE_NAME="povo-server"
REGION="us-central1"  # Change to your preferred region

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}☁️  Deploying to Google Cloud Run...${NC}"

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
# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY is not set.${NC}"
    echo "The service will run in demo mode without actual AI responses."
    echo "To set it, run: export OPENAI_API_KEY=your_key_here"
    echo "Or the service will be deployed without the API key (demo mode)."
    echo ""
    ENV_VARS="ENV=production"
else
    echo -e "${GREEN}✅ OPENAI_API_KEY is set${NC}"
    ENV_VARS="ENV=production,OPENAI_API_KEY=$OPENAI_API_KEY"
fi

gcloud services enable cloudbuild.googleapis.com

# Deploy to Cloud Run
echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
  --image=$DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG \
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
curl -f "$SERVICE_URL/health" || echo -e "${YELLOW}Health check endpoint not available${NC}"

echo -e "${GREEN}🎉 Deployment successful!${NC}"
