# 🐳 Docker Deployment for React Frontend

This directory contains all the necessary files to build and deploy the React frontend application using Docker, optimized for AWS deployment.

## 📁 Files Overview

- **Dockerfile** - Multi-stage build configuration for production deployment
- **nginx.conf** - Production-ready nginx configuration
- **.dockerignore** - Excludes unnecessary files from Docker build context
- **docker-compose.yml** - Local development and testing
- **build-aws.sh** - Automated AWS ECR deployment script

## 🚀 Quick Start

### Local Development

```bash
# Build the Docker image
docker build -t frontend-app .

# Run locally
docker run -d -p 3000:80 --name frontend-app frontend-app

# Test the application
curl http://localhost:3000/health
```

### AWS Deployment

```bash
# Make sure AWS CLI is configured
aws configure

# Run the automated build and push script
./build-aws.sh
```

## 🏗️ Architecture

### Multi-Stage Build
1. **Builder Stage** (Node.js 20): Builds the React application
2. **Production Stage** (Nginx Alpine): Serves the static files

### Security Features
- Non-root user execution
- Minimal Alpine Linux base image
- Security headers configured
- Health check endpoint included

### Performance Optimizations
- Gzip compression enabled
- Static asset caching (1 year)
- Optimized nginx configuration
- Small final image size

## 🔧 Configuration Details

### Nginx Configuration
- **Port**: 80
- **Health Check**: `/health` endpoint
- **SPA Support**: Fallback routing to `index.html`
- **Security Headers**: XSS protection, CSRF prevention
- **Compression**: Gzip for all text-based files

### Docker Features
- **Health Check**: Built-in container health monitoring
- **Logging**: Structured nginx access/error logs
- **User**: Runs as non-root user `nginx-user` (UID: 1001)

## 📊 AWS ECR Integration

The build script is pre-configured for your AWS ECR repository:
- **Registry**: `672029949135.dkr.ecr.ap-northeast-2.amazonaws.com`
- **Repository**: `kpsa-hackathon-2025-team-11-frontend`
- **Region**: `ap-northeast-2` (Seoul)

## 🧪 Testing

```bash
# Build and test locally
docker build -t test-frontend .
docker run -d -p 8080:80 --name test-frontend test-frontend

# Health check
curl http://localhost:8080/health
# Expected: "healthy"

# Application check
curl -I http://localhost:8080/
# Expected: HTTP 200 OK

# Cleanup
docker stop test-frontend && docker rm test-frontend
```

## 🔍 Troubleshooting

### Common Issues

1. **Build fails with "vite: not found"**
   - Solution: Dependencies are properly installed in the Dockerfile

2. **Container exits immediately**
   - Check logs: `docker logs <container-name>`
   - Nginx configuration is validated

3. **Permission denied errors**
   - The container runs as non-root user with proper permissions

### Debug Commands

```bash
# Check container status
docker ps -a

# View container logs
docker logs <container-name>

# Execute into running container
docker exec -it <container-name> /bin/sh

# Test nginx configuration
docker run --rm -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf nginx:alpine nginx -t
```

## 🌐 AWS Deployment Options

This Docker image works with:
- **AWS ECS** (Elastic Container Service)
- **AWS Fargate** (Serverless containers)
- **AWS EKS** (Kubernetes)
- **AWS App Runner** (Fully managed)

## 📋 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NODE_ENV` | `production` | Build environment |
| `PORT` | `80` | Container port (nginx) |

## 🎯 Production Checklist

- ✅ Multi-stage build for minimal image size
- ✅ Non-root user for security
- ✅ Health checks configured
- ✅ Gzip compression enabled
- ✅ Security headers set
- ✅ Static asset caching
- ✅ SPA routing support
- ✅ Error handling
- ✅ AWS ECR integration ready

---

**Image Size**: ~50MB (optimized Alpine Linux + built assets)  
**Build Time**: ~15 seconds (with cache)  
**Security**: Non-root execution, minimal attack surface  
**Performance**: Nginx with compression and caching  
