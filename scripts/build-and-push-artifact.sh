#!/bin/bash
set -e

# Configuration - UPDATE THESE VALUES
PROJECT_ID="povo-demo"  # Replace with your GCP project ID
REGION="us-central1"  # Change to your preferred region
REPOSITORY="povo"  # Artifact Registry repository name
IMAGE_NAME="povo-server"
TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Building and pushing to Google Artifact Registry...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

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
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Create Artifact Registry repository if it doesn't exist
echo -e "${YELLOW}📦 Creating Artifact Registry repository...${NC}"
gcloud artifacts repositories create $REPOSITORY \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for Povo chatbot" \
    --quiet || echo "Repository already exists"

# Configure Docker authentication for Artifact Registry
echo -e "${YELLOW}🔑 Configuring Docker authentication...${NC}"
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

# Build the image with Artifact Registry tag
FULL_IMAGE_NAME="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$TAG"
echo -e "${YELLOW}🔨 Building Docker image: $FULL_IMAGE_NAME${NC}"
docker build -t $FULL_IMAGE_NAME .

# Push to Artifact Registry
echo -e "${YELLOW}📤 Pushing to Artifact Registry...${NC}"
docker push $FULL_IMAGE_NAME

echo -e "${GREEN}✅ Successfully pushed to Google Artifact Registry!${NC}"
echo -e "${GREEN}Image: $FULL_IMAGE_NAME${NC}"

# Test locally (optional)
echo -e "${YELLOW}🧪 To test locally, run:${NC}"
echo "# With environment file:"
echo "docker run -p 8080:8080 --env-file .env $FULL_IMAGE_NAME"
echo ""
echo "# Or with individual environment variables:"
echo "docker run -p 8080:8080 -e OPENAI_API_KEY=your_key_here $FULL_IMAGE_NAME"
echo ""
echo -e "${GREEN}Visit http://localhost:8080/docs to test the API${NC}"
echo ""
echo -e "${YELLOW}🚀 To deploy to Cloud Run, run:${NC}"
echo "./deploy-cloudrun-from-artifact.sh"
