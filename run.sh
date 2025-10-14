#!/bin/bash

##################################
# SERVICE CONFIGURATION
# Set to true to enable, false to disable
##################################
ENABLE_N8N=true
ENABLE_OPENWEBUI=true
ENABLE_FLOWISE=true
ENABLE_QDRANT=true
ENABLE_NEO4J=true
ENABLE_LANGFUSE=true
ENABLE_PORTAINER=true

##################################
# Build profile arguments
##################################
PROFILES=""
[ "$ENABLE_N8N" = true ] && PROFILES="$PROFILES --profile n8n"
[ "$ENABLE_OPENWEBUI" = true ] && PROFILES="$PROFILES --profile openwebui"
[ "$ENABLE_FLOWISE" = true ] && PROFILES="$PROFILES --profile flowise"
[ "$ENABLE_QDRANT" = true ] && PROFILES="$PROFILES --profile qdrant"
[ "$ENABLE_NEO4J" = true ] && PROFILES="$PROFILES --profile neo4j"
[ "$ENABLE_LANGFUSE" = true ] && PROFILES="$PROFILES --profile langfuse"
[ "$ENABLE_PORTAINER" = true ] && PROFILES="$PROFILES --profile portainer"

##################################
# Execute commands
##################################

# Stop all services
echo "Stopping all services..."
docker compose -p localai -f docker-compose.yml $PROFILES down

# Pull latest versions of all containers
echo "Pulling latest versions..."
docker compose -p localai -f docker-compose.yml $PROFILES pull

# Start services with selected profiles
echo "Starting services..."
python3 start_services.py $PROFILES
