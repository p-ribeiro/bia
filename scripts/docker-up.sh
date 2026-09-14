#!/usr/bin/env bash
# Start this worktree's app stack, isolated from every other worktree's stack.
# Run from anywhere inside the task's worktree.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
# shellcheck source=./docker-env.sh
source "$(dirname "${BASH_SOURCE[0]}")/docker-env.sh"

echo "Project: $COMPOSE_PROJECT_NAME | server:$HOST_SERVER_PORT db:$HOST_DB_PORT redis:$HOST_REDIS_PORT"
docker compose up -d --build
