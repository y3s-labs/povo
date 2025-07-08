# Docker Hub and Cloud Run Deployment Guide

This gui### Step 3: Build and ### Step 4: Deploy to Cloud Run
```bash
# Make sure your API key is set (if you want full functionality)
export OPENAI_API_KEY="your-openai-api-key-here"

# Run the Cloud Run deployment script
./scripts/deploy-cloudrun.sh
```

This will:
- Authenticate with Google Cloud (if needed)
- Enable required APIs
- Deploy your container to Cloud Run (with or without API key)
- Provide your service URLker Hub
```bash
# Run the build and push script
./scripts/build-and-push.sh
```

This will:
- Build your Docker image
- Push it to Docker Hub
- Show you how to test locally (with and without API key)

### Step 4: Deploy to Cloud Run you deploy the Povo Chatbot to Docker Hub and Google Cloud Run.

## Prerequisites

### 1. OpenAI API Key
- Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- The application will run in demo mode without it, but you need it for full functionality

### 2. Docker Hub Account
- Create an account at [Docker Hub](https://hub.docker.com)
- Note your Docker Hub username

### 3. Google Cloud Platform Setup
- Create a GCP project at [Google Cloud Console](https://console.cloud.google.com)
- Enable billing for your project
- Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- Note your project ID

### 3. Local Requirements
- Docker installed and running
- Google Cloud CLI installed
- Terminal access

## Quick Deployment

### Step 1: Configure Your Settings
Edit the configuration variables in both scripts:

**In `scripts/build-and-push.sh`:**
```bash
DOCKER_HUB_USERNAME="your-dockerhub-username"  # Replace with your Docker Hub username
```

**In `scripts/deploy-cloudrun.sh`:**
```bash
DOCKER_HUB_USERNAME="your-dockerhub-username"  # Replace with your Docker Hub username
PROJECT_ID="your-gcp-project-id"              # Replace with your GCP project ID
REGION="us-central1"                           # Change to your preferred region
```

### Step 2: Set Your OpenAI API Key (Optional)
```bash
# Set your OpenAI API key for full functionality
export OPENAI_API_KEY="your-openai-api-key-here"

# Or create a .env file in the project root:
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

**Note**: The service will run in demo mode without the API key, but you'll get mock responses instead of real AI responses.

### Step 3: Build and Push to Docker Hub
```bash
# Run the build and push script
./scripts/build-and-push.sh
```

This will:
- Build your Docker image
- Push it to Docker Hub
- Show you how to test locally

### Step 3: Deploy to Cloud Run
```bash
# Run the Cloud Run deployment script
./scripts/deploy-cloudrun.sh
```

This will:
- Authenticate with Google Cloud (if needed)
- Enable required APIs
- Deploy your container to Cloud Run
- Provide your service URL

## Google Artifact Registry Deployment (Recommended)

Google Artifact Registry is the recommended approach for deploying to Cloud Run as it's more integrated with Google Cloud services and provides better security and performance.

### Quick Start with Artifact Registry

1. **Configure your project ID** in the scripts:
   ```bash
   # Edit scripts/build-and-push-artifact.sh
   PROJECT_ID="your-gcp-project-id"
   REGION="us-central1"
   ```

2. **Run the complete deployment**:
   ```bash
   ./scripts/complete-artifact-deploy.sh
   ```

This single command will:
- Create an Artifact Registry repository
- Build your Docker image
- Push it to Artifact Registry
- Deploy to Cloud Run
- Automatically include your `.env` file variables

### Individual Steps with Artifact Registry

If you prefer to run steps individually:

```bash
# Step 1: Build and push to Artifact Registry
./scripts/build-and-push-artifact.sh

# Step 2: Deploy to Cloud Run
./scripts/deploy-cloudrun-from-artifact.sh
```

### Environment Variables with Artifact Registry

The Artifact Registry deployment scripts automatically:
- Read your `.env` file
- Include all environment variables in the Cloud Run deployment
- Handle the `OPENAI_API_KEY` and other secrets securely

**No manual environment variable configuration needed!**

---

## Manual Step-by-Step Process

### 1. Build Docker Image
```bash
# Build the image
docker build -t your-dockerhub-username/povo-server:latest .

# Test locally without API key (demo mode)
docker run -p 8080:8080 your-dockerhub-username/povo-server:latest

# Test locally with API key (full functionality)
docker run -p 8080:8080 -e OPENAI_API_KEY=your_key_here your-dockerhub-username/povo-server:latest
```

### 2. Push to Docker Hub
```bash
# Log into Docker Hub
docker login

# Push the image
docker push your-dockerhub-username/povo-server:latest
```

### 3. Deploy to Cloud Run
```bash
# Authenticate with Google Cloud
gcloud auth login

# Set your project
gcloud config set project your-gcp-project-id

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Deploy to Cloud Run (with API key)
gcloud run deploy povo-server \
  --image=your-dockerhub-username/povo-server:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8080 \
  --memory=1Gi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --timeout=300 \
  --set-env-vars="ENV=production,OPENAI_API_KEY=your_openai_api_key_here"

# Or deploy without API key (demo mode)
gcloud run deploy povo-server \
  --image=your-dockerhub-username/povo-server:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8080 \
  --memory=1Gi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --timeout=300 \
  --set-env-vars="ENV=production"
```

## Environment Variables

If your application requires environment variables, add them to the deployment:

```bash
gcloud run deploy povo-server \
  --image=your-dockerhub-username/povo-server:latest \
  --set-env-vars="ENV=production,OPENAI_API_KEY=your-key,ANOTHER_VAR=value"
```

## Testing Your Deployment

### 1. Health Check
```bash
curl https://your-service-url/health
```

### 2. API Documentation
Visit: `https://your-service-url/docs`

### 3. Test Chat Endpoint
```bash
curl -X POST "https://your-service-url/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "message": {
        "role": "user",
        "content": "Hello, I love pizza!"
      },
      "session": {
        "id": "test-session",
        "data": {}
      },
      "user": {
        "id": "test-user",
        "data": {}
      }
    }
  }'
```

## Troubleshooting

### Common Issues

1. **Docker build fails**: Make sure Docker is running and you're in the project root
2. **Push fails**: Make sure you're logged into Docker Hub (`docker login`)
3. **Cloud Run deployment fails**: Check your GCP project ID and ensure billing is enabled
4. **Service not responding**: Check logs with `gcloud run logs read --service=povo-server`

### Checking Logs
```bash
# View Cloud Run logs
gcloud run logs read --service=povo-server --region=us-central1

# Follow logs in real-time
gcloud run logs tail --service=povo-server --region=us-central1
```

### Update Deployment
To update your deployment with a new version:
```bash
# Build and push new image
./scripts/build-and-push.sh

# Redeploy
./scripts/deploy-cloudrun.sh
```

## Cost Optimization

Cloud Run charges based on:
- CPU and memory usage
- Number of requests
- Request duration

The current configuration:
- `--min-instances=0`: Scales to zero when not in use
- `--max-instances=10`: Limits maximum scale
- `--memory=1Gi --cpu=1`: Appropriate for most chatbot workloads

## Security

- The service is deployed with `--allow-unauthenticated` for easy access
- For production, consider implementing proper authentication
- Environment variables are securely managed by Cloud Run
- Use secrets manager for sensitive data

## Next Steps

1. Set up custom domain
2. Configure SSL certificate
3. Set up monitoring and alerting
4. Implement CI/CD pipeline
5. Add authentication if needed

Your chatbot is now deployed and ready to use! 🚀
