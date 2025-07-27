#!/bin/bash

# Build script for AWS deployment
set -e

echo "🚀 Building React frontend for AWS deployment..."

# Set build environment
export NODE_ENV=production

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t frontend-app:latest .

# Tag for AWS ECR (replace with your actual ECR repository)
echo "🏷️  Tagging image for ECR..."
docker tag frontend-app:latest 672029949135.dkr.ecr.ap-northeast-2.amazonaws.com/kpsa-hackathon-2025-team-11-frontend:latest

# Push to ECR (uncomment after configuring ECR)
echo "☁️  Pushing to ECR..."
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 672029949135.dkr.ecr.ap-northeast-2.amazonaws.com
docker push 672029949135.dkr.ecr.ap-northeast-2.amazonaws.com/kpsa-hackathon-2025-team-11-frontend:latest

echo "✅ Build and push completed successfully!"
echo "💡 Your image is now available in ECR:"
echo "   672029949135.dkr.ecr.ap-northeast-2.amazonaws.com/kpsa-hackathon-2025-team-11-frontend:latest"
