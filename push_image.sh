#!/bin/bash

# Build Docker image from Dockerfile
docker build -t backend-sipemas .

# Display a list of available Docker images locally
docker images

# Login to Docker Hub
echo "Enter your Docker Hub username:"
read -p "Username: " username
echo "Enter your Docker Hub password:"
read -s password
echo
docker login -u $username -p $password

# Tag and push the image to Docker Hub
docker tag backend-sipemas:latest mikasuryof/backend-sipemas:latest
docker push mikasuryof/backend-sipemas:latest

# Clean up: Remove local image (optional)
docker rmi backend-sipemas:latest
