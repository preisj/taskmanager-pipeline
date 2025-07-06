#!/bin/bash

set -e

PROD_USER=ubuntu
PROD_HOST=your.production.server.ip
PROD_PATH=/home/ubuntu/taskmanager-prod

echo "🚀 Deploying to Produção..."

rsync -avz --exclude '__pycache__' --exclude '.git' --exclude 'venv' ./ $PROD_USER@$PROD_HOST:$PROD_PATH

ssh $PROD_USER@$PROD_HOST << EOF
  cd $PROD_PATH
  docker compose down
  docker compose up -d --build
  echo "✅ Production deployment complete."
EOF
