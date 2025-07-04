#!/bin/bash

echo "[INFO] Shutting down current containers..."
docker-compose down

echo "[INFO] Building and starting containers..."
docker-compose up -d --build
