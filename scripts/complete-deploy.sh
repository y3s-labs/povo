#!/bin/bash
set -e

# Load configuration
CONFIG_FILE="deployment-config.sh"
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
    echo "✅ Loaded configuration from $CONFIG_FILE"
else
    echo "❌ Configuration file $CONFIG_FILE not found!"
    echo "Please copy deployment-config.example.sh to deployment-config.sh and update with your values"
    exit 1
fi

# Validate required variables
required_vars=("DOCKER_HUB_USERNAME" "PROJECT_ID" "SERVICE_NAME" "REGION")
for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "❌ Required variable $var is not set in $CONFIG_FILE"
        exit 1
    fi
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Complete Deployment: Docker Hub → Cloud Run${NC}"
echo -e "${YELLOW}Configuration:${NC}"
echo -e "  Docker Hub: $DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG"
echo -e "  GCP Project: $PROJECT_ID"
echo -e "  Service: $SERVICE_NAME"
echo -e "  Region: $REGION"
echo ""

# Step 1: Build and push to Docker Hub
echo -e "${YELLOW}📦 Step 1: Building and pushing to Docker Hub...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Build the image
echo -e "${YELLOW}🔨 Building Docker image...${NC}"
docker build -t $DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG .

# Check if user is logged into Docker Hub
if ! docker info 2>/dev/null | grep -q "Username"; then
    echo -e "${YELLOW}🔐 Please log into Docker Hub:${NC}"
    docker login
fi

# Push to Docker Hub
echo -e "${YELLOW}📤 Pushing to Docker Hub...${NC}"
docker push $DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG

echo -e "${GREEN}✅ Successfully pushed to Docker Hub!${NC}"

# Step 2: Deploy to Cloud Run
echo -e "${YELLOW}☁️  Step 2: Deploying to Cloud Run...${NC}"

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
gcloud services enable cloudbuild.googleapis.com

# Deploy to Cloud Run
echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
  --image=$DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --port=$PORT \
  --memory=$MEMORY \
  --cpu=$CPU \
  --min-instances=$MIN_INSTANCES \
  --max-instances=$MAX_INSTANCES \
  --timeout=$TIMEOUT \
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
