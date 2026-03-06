#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"

docker compose -f docker-compose.observability.yml down

Write-Host "LGTM stack stopped." -ForegroundColor Yellow
