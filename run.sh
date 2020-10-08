#!/bin/bash
# Run flask server

# Update codes
# Still need gitlab ID and PW (will be updated)
git checkout feature/link_app
git pull

# Run docker-compose
sudo docker-compose up -d