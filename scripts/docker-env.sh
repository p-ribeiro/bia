#!/usr/bin/env bash
# Source this file (do not execute) from inside a task's git worktree to compute
# a Docker Compose project name and host ports that won't collide with any other
# worktree's stack running on the same machine at the same time.
#
# Isolation scheme:
# - COMPOSE_PROJECT_NAME is derived from the branch name, so containers, networks
#   and volumes are namespaced per task instead of colliding on shared names.
# - Host ports are offset by the task number embedded in the branch name
#   (e.g. feature/012-login_button -> 12), so each task gets its own port range
#   without needing manual coordination between agents.
set -euo pipefail

BRANCH="$(git branch --show-current)"
if [ -z "$BRANCH" ]; then
  echo "docker-env.sh: could not determine current git branch (detached HEAD?)" >&2
  exit 1
fi

TASK_NUMBER="$(echo "$BRANCH" | grep -oE '[0-9]+' | head -1 || true)"
TASK_NUMBER="${TASK_NUMBER:-0}"
TASK_NUMBER=$((10#$TASK_NUMBER))

SAFE_BRANCH="$(printf '%s' "$BRANCH" | tr '/_' '--' | tr -cd '[:alnum:]-')"

export COMPOSE_PROJECT_NAME="bia-${SAFE_BRANCH}"
export HOST_SERVER_PORT=$((3000 + TASK_NUMBER))
export HOST_DB_PORT=$((5400 + TASK_NUMBER))
export HOST_REDIS_PORT=$((6300 + TASK_NUMBER))
