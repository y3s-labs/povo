#!/bin/bash
set -e

# Configuration - UPDATE THESE VALUES
DOCKER_HUB_USERNAME="marcher357"  # Replace with your Docker Hub username
IMAGE_NAME="povo-server"
TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐳 Building and pushing Docker image to Docker Hub...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Build the image
echo -e "${YELLOW}📦 Building Docker image: $DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG${NC}"
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
echo -e "${GREEN}Image: $DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG${NC}"

# Test locally (optional)
echo -e "${YELLOW}🧪 To test locally, run:${NC}"
echo "# For demo mode (without OpenAI API key):"
echo "docker run -p 8080:8080 $DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG"
echo ""
echo "# With OpenAI API key:"
echo "docker run -p 8080:8080 -e OPENAI_API_KEY=your_openai_api_key_here $DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG"
echo ""
echo "# Or with environment file:"
echo "docker run -p 8080:8080 --env-file .env $DOCKER_HUB_USERNAME/$IMAGE_NAME:$TAG"
echo ""
echo -e "${GREEN}Visit http://localhost:8080/docs to test the API${NC}"
