#!/bin/bash

echo "🧹 Running cleanup..."

docker image prune -f

rm -f /home/ubuntu/taskmanager-prod/logs/*.log

echo "✅ Cleanup complete."
