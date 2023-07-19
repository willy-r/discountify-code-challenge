#!/bin/bash

docker compose -f ./docker/docker-compose.dev.yml exec -d api-fastapi alembic upgrade head
