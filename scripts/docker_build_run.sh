#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

if [ -z "$1" ]; then
  echo -e "${RED}Please provide an image version argument.${NC}"
  exit 1
fi

echo -e "${GREEN}Running 'docker build' command:${NC}"
docker build --platform=linux/amd64 -t <your_image>:$1 .

echo -e "${GREEN}Running 'docker run' command:${NC}"
docker run --platform=linux/amd64 -p 80:80 -d \
  -e OPENAI_API_KEY="<OPENAI_API_KEY>" \
  -e OPENAI_API_TYPE="<OPENAI_API_TYPE>" \
  -e OPENAI_API_BASE="<OPENAI_API_BASE>" \
  -e OPENAI_API_DEPLOYMENT="<OPENAI_API_DEPLOYMENT>" \
  <your_image>:$1

echo -e "${GREEN}Running 'docker login' command:${NC}"
docker login

echo -e "${GREEN}Running 'docker tag' command:${NC}"
docker tag gen-qa-forge-api:$1 <your_username>/<your_image>:$1

echo -e "${GREEN}Running 'docker push' command:${NC}"
docker push <your_username>/<your_repo>:$1