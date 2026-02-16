#!/usr/bin/env pwsh

Write-Host "Setting environment variables..." -ForegroundColor Cyan
$env:HEADLESS = "true"
$env:API_BASE_URL = "https://jsonplaceholder.typicode.com"

Write-Host "Installing Playwright browsers..." -ForegroundColor Cyan
playwright install

Write-Host "Running tests with pytest..." -ForegroundColor Cyan
python -m pytest -v --headless=true

Write-Host "Starting Allure report server..." -ForegroundColor Cyan
allure serve allure-results
