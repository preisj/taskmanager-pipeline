#!/bin/bash

set -e

STAGING_USER=ubuntu
STAGING_HOST=your.staging.server.ip
STAGING_PATH=/home/ubuntu/taskmanager-staging

echo "🔁 Deploying to Homologação (Staging)..."

rsync -avz --exclude '__pycache__' --exclude '.git' --exclude 'venv' ./ $STAGING_USER@$STAGING_HOST:$STAGING_PATH

ssh $STAGING_USER@$STAGING_HOST << EOF
  cd $STAGING_PATH
  docker compose down
  docker compose up -d --build
  echo "✅ Staging deployment complete."
EOF
