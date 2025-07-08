#!/bin/bash
set -e

# Configuration
DOCKER_HUB_USERNAME="your-dockerhub-username"  # Replace with your Docker Hub username
IMAGE_NAME="povo-chatbot"
PROJECT_ID="your-gcp-project-id"  # Replace with your GCP project ID
SERVICE_NAME="povo-chatbot"
REGION="us-central1"  # Change to your preferred region

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Docker Hub and Cloud Run deployment...${NC}"

# Step 1: Build the Docker image
echo -e "${YELLOW}📦 Building Docker image...${NC}"
docker build -t $DOCKER_HUB_USERNAME/$IMAGE_NAME:latest .

# Step 2: Test the image locally (optional)
echo -e "${YELLOW}🧪 Testing image locally...${NC}"
echo "You can test the image locally by running:"
echo "docker run -p 8080:8080 $DOCKER_HUB_USERNAME/$IMAGE_NAME:latest"
read -p "Press Enter to continue or Ctrl+C to exit and test locally..."

# Step 3: Push to Docker Hub
echo -e "${YELLOW}📤 Pushing to Docker Hub...${NC}"
echo "Please make sure you're logged into Docker Hub (run 'docker login' if needed)"
docker push $DOCKER_HUB_USERNAME/$IMAGE_NAME:latest

# Step 4: Deploy to Cloud Run
echo -e "${YELLOW}☁️  Deploying to Cloud Run...${NC}"
echo "Please make sure you're authenticated with GCP (run 'gcloud auth login' if needed)"
echo "And that your project is set (run 'gcloud config set project $PROJECT_ID')"

gcloud run deploy $SERVICE_NAME \
  --image=$DOCKER_HUB_USERNAME/$IMAGE_NAME:latest \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --port=8080 \
  --memory=1Gi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --timeout=300

echo -e "${GREEN}✅ Deployment completed!${NC}"
echo -e "${GREEN}Your service is available at:${NC}"
gcloud run services describe $SERVICE_NAME --platform=managed --region=$REGION --format='value(status.url)'
