#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"

docker compose -f docker-compose.observability.yml up -d

Write-Host "LGTM stack started." -ForegroundColor Green
Write-Host "Grafana: http://localhost:3000 (admin/admin)"
Write-Host "Loki: http://localhost:3100"
Write-Host "Tempo: http://localhost:3200"
Write-Host "Prometheus: http://localhost:9090"
