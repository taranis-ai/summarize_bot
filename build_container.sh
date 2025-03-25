#!/bin/bash

set -eou pipefail

cd $(git rev-parse --show-toplevel)

GITHUB_REPOSITORY_OWNER=${GITHUB_REPOSITORY_OWNER:-"ghcr.io/taranis-ai"}
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD | sed 's/[^a-zA-Z0-9_.-]/_/g')
MODEL=${MODEL:-"t5"}

echo "Building containers for branch ${CURRENT_BRANCH} with model ${MODEL} on ${GITHUB_REPOSITORY_OWNER}"

docker buildx build --file Containerfile \
  --build-arg GITHUB_REPOSITORY_OWNER="${GITHUB_REPOSITORY_OWNER}" \
  --build-arg MODEL="${MODEL}" \
  --tag "${GITHUB_REPOSITORY_OWNER}/taranis-summarize-bot:latest" \
  --tag "${GITHUB_REPOSITORY_OWNER}/taranis-summarize-bot:${CURRENT_BRANCH}" \
  --tag "${GITHUB_REPOSITORY_OWNER}/taranis-summarize-bot:${MODEL}" \
  --load .

