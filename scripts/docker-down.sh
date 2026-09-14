#!/usr/bin/env bash
# Tear down this worktree's app stack (containers, network). Run from anywhere
# inside the task's worktree. Leaves the shared image cache and other
# worktrees' stacks untouched.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
# shellcheck source=./docker-env.sh
source "$(dirname "${BASH_SOURCE[0]}")/docker-env.sh"

docker compose down
