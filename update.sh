# Stop all services
docker compose -p localai -f docker-compose.yml --profile none down

# Pull latest versions of all containers
docker compose -p localai -f docker-compose.yml --profile none pull

# Start services again with your desired profile
./run.sh