#!/bin/bash

# Check if .env file exists
if [ -f .env ]; then
  # Export variables from .env file
  export $(grep -v '^#' .env | xargs)
fi

# Export additional environment variables
export IMAGE_TAG="latest"
export APP_FOLDER_NAME="instavibe"
export IMAGE_NAME="instavibe-webapp"
# Note: Ensure REGION, PROJECT_ID, and REPO_NAME are set in your .env or environment
export IMAGE_PATH="${GOOGLE_CLOUD_LOCATION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG}"
export SERVICE_NAME="instavibe"


# Check if required variables are set
if [ -z "$GOOGLE_CLOUD_PROJECT" ] || [ -z "$GOOGLE_CLOUD_LOCATION" ] || [ -z "$REPO_NAME" ]; then
  echo "Error: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, and REPO_NAME must be set in the .env file."
  exit 1
fi


echo ${SPANNER_INSTANCE_ID}
echo ${SPANNER_DATABASE_ID}
echo ${REPO_NAME}

# Run the gcloud build command
gcloud builds submit . \
  --tag="${IMAGE_PATH}" \
  --project="${GOOGLE_CLOUD_PROJECT}"



gcloud run deploy ${SERVICE_NAME} \
  --image=${IMAGE_PATH} \
  --platform=managed \
  --region=${GOOGLE_CLOUD_LOCATION} \
  --allow-unauthenticated \
  --set-env-vars="SPANNER_INSTANCE_ID=${SPANNER_INSTANCE_ID}" \
  --set-env-vars="SPANNER_DATABASE_ID=${SPANNER_DATABASE_ID}" \
  --set-env-vars="APP_HOST=0.0.0.0" \
  --set-env-vars="APP_PORT=8080" \
  --set-env-vars="GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION}" \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
  --set-env-vars="GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}" \
  --project=${GOOGLE_CLOUD_PROJECT} \
  --min-instances=1

