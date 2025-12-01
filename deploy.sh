#!/bin/bash

# Production deployment script for Südwest-Energie Website

set -e  # Exit immediately if a command exits with a non-zero status

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Südwest-Energie - Production Deployment Script${NC}"
echo -e "${YELLOW}==================================================${NC}"

# Check if we're in the right directory
if [ ! -f "rxconfig.py" ]; then
    echo -e "${RED}Error: rxconfig.py not found. Please run this script from the project root.${NC}"
    exit 1
fi

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not in PATH.${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}Error: Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Warning: docker-compose not found. Using 'docker compose' (newer version).${NC}"
    DOCKER_COMPOSE_CMD="docker compose"
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo -e "${GREEN}Environment checks passed.${NC}"

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Copying from .env.example${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please update the .env file with your production values before proceeding.${NC}"
    exit 1
fi

# Build and deploy
echo -e "${GREEN}Starting production build and deployment...${NC}"

# Build the application
echo -e "${GREEN}Building Docker images...${NC}"
$DOCKER_COMPOSE_CMD build

# Run database migrations (if any)
echo -e "${GREEN}Starting database service...${NC}"
$DOCKER_COMPOSE_CMD up -d db

# Wait for database to be ready
echo -e "${GREEN}Waiting for database to be ready...${NC}"
sleep 10

# Start the application
echo -e "${GREEN}Starting application...${NC}"
$DOCKER_COMPOSE_CMD up -d

# Wait for application to start
echo -e "${GREEN}Waiting for application to start...${NC}"
sleep 15

# Run health check
echo -e "${GREEN}Running health check...${NC}"
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Application is running successfully!${NC}"
else
    echo -e "${RED}❌ Application health check failed${NC}"
    echo -e "${YELLOW}Check logs with: $DOCKER_COMPOSE_CMD logs${NC}"
fi

echo -e "${GREEN}Deployment completed.${NC}"
echo -e "${GREEN}The application should be accessible at http://localhost or your configured domain.${NC}"
echo -e "${YELLOW}To view logs: $DOCKER_COMPOSE_CMD logs -f${NC}"
echo -e "${YELLOW}To stop the application: $DOCKER_COMPOSE_CMD down${NC}"