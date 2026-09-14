#!/usr/bin/env bash
# Rebuild and restart just the server container for this worktree, picking up
# code changes. Run from anywhere inside the task's worktree.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
# shellcheck source=./docker-env.sh
source "$(dirname "${BASH_SOURCE[0]}")/docker-env.sh"

docker compose up -d --build server
