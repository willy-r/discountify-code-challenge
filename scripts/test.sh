#!/bin/bash

docker compose -f ./docker/docker-compose.dev.yml exec api-fastapi pytest -s -x --cov=app -vv
