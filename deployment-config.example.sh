# Deployment Configuration
# Copy this file to deployment-config.sh and update with your values

# Docker Hub Configuration
export DOCKER_HUB_USERNAME="your-dockerhub-username"
export IMAGE_NAME="povo-server"
export TAG="latest"

# Google Cloud Configuration
export PROJECT_ID="your-gcp-project-id"
export SERVICE_NAME="povo-server"
export REGION="us-central1"

# Cloud Run Configuration
export MEMORY="1Gi"
export CPU="1"
export MIN_INSTANCES="0"
export MAX_INSTANCES="10"
export TIMEOUT="300"
export PORT="8080"

# Environment Variables for the deployed service
export ENV_VARS="ENV=production"

# Optional: Add your API keys or other environment variables
# export ENV_VARS="ENV=production,OPENAI_API_KEY=your-key,GOOGLE_API_KEY=your-key"
