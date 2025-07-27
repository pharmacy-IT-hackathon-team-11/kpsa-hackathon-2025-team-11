#!/bin/bash

# Build Docker image with platform specification using buildx
# This script helps prevent exec format errors by explicitly setting the platform

set -e

# Get current platform
PLATFORM=$(uname -m)
case $PLATFORM in
    x86_64)
        DOCKER_PLATFORM="linux/amd64"
        ;;
    arm64|aarch64)
        DOCKER_PLATFORM="linux/arm64"
        ;;
    *)
        echo "Unknown platform: $PLATFORM"
        echo "Defaulting to linux/amd64"
        DOCKER_PLATFORM="linux/amd64"
        ;;
esac

echo "Building for platform: $DOCKER_PLATFORM"

# Ensure buildx is available
if ! docker buildx version &> /dev/null; then
    echo "Error: Docker buildx is not available. Please install Docker Desktop or enable buildx."
    exit 1
fi

# Create and use a new builder instance if needed
BUILDER_NAME="multiplatform-builder"
if ! docker buildx inspect $BUILDER_NAME &> /dev/null; then
    echo "Creating new buildx builder: $BUILDER_NAME"
    docker buildx create --name $BUILDER_NAME --driver docker-container --bootstrap
fi

docker buildx use $BUILDER_NAME

# Build the Docker image
echo "Building Docker image..."
docker buildx build \
    --platform $DOCKER_PLATFORM \
    --load \
    -t dnable-frontend:latest \
    .

echo "Build completed successfully!"
echo "To run the container:"
echo "docker run --platform $DOCKER_PLATFORM -p 80:80 dnable-frontend:latest"
