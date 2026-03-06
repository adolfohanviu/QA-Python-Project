#!/bin/bash

set -euo pipefail

docker compose -f docker-compose.observability.yml down

echo "LGTM stack stopped."
