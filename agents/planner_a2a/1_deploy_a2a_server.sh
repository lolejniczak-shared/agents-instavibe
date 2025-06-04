#!/bin/bash

# Check if .env file exists
if [ -f .env ]; then
  # Export variables from .env file
  export $(grep -v '^#' .env | xargs)
fi

# Export additional environment variables
IMAGE_TAG="latest"
IMAGE_NAME="planner-agent"
# Note: Ensure REGION, PROJECT_ID, and REPO_NAME are set in your .env or environment
IMAGE_PATH="${GOOGLE_CLOUD_LOCATION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG}"
AGENT_NAME="planner-agent"
SERVICE_NAME="planner-agent"
A2A_PUBLIC_URL="https://planner-agent-${GOOGLE_CLOUD_PROJECT_NUMBER}.${GOOGLE_CLOUD_LOCATION}.run.app"

# Check if required variables are set
if [ -z "$GOOGLE_CLOUD_PROJECT" ] || [ -z "$GOOGLE_CLOUD_LOCATION" ] || [ -z "$REPO_NAME" ]; then
  echo "Error: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, and REPO_NAME must be set in the .env file."
  exit 1
fi


echo "Building ${AGENT_NAME} agent..."
gcloud builds submit . \
  --tag=${IMAGE_PATH} \
  --project=${GOOGLE_CLOUD_PROJECT}

echo "Image built and pushed to: ${IMAGE_PATH}"

gcloud run deploy ${SERVICE_NAME} \
  --image=${IMAGE_PATH} \
  --platform=managed \
  --region=${GOOGLE_CLOUD_LOCATION} \
  --set-env-vars="A2A_HOST=0.0.0.0" \
  --set-env-vars="A2A_PORT=8080" \
  --set-env-vars="A2A_PUBLIC_URL=${A2A_PUBLIC_URL}" \
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=TRUE" \
  --set-env-vars="GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION}" \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
  --set-env-vars="PUBLIC_URL=${A2A_PUBLIC_URL}" \
  --allow-unauthenticated \
  --project=${GOOGLE_CLOUD_PROJECT} \
  --min-instances=1


