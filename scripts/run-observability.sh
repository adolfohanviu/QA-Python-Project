#!/bin/bash

set -euo pipefail

docker compose -f docker-compose.observability.yml up -d

echo "LGTM stack started."
echo "Grafana: http://localhost:3000 (admin/admin)"
echo "Loki: http://localhost:3100"
echo "Tempo: http://localhost:3200"
echo "Prometheus: http://localhost:9090"
