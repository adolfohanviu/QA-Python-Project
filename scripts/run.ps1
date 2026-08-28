#!/usr/bin/env pwsh

# PowerShell does not stop, or fail its own exit code, on a failing native
# command by default - each install step is checked explicitly so this
# script fails fast on a broken setup the same way run.sh's `set -e` does.
function Assert-Success {
    param([string]$Step)
    if ($LASTEXITCODE -ne 0) {
        Write-Error "$Step failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
}

Write-Host "Setting environment variables..." -ForegroundColor Cyan
$env:HEADLESS = "true"
$env:API_BASE_URL = "https://jsonplaceholder.typicode.com"

Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
Assert-Success "pip install"

Write-Host "Installing Playwright browsers..." -ForegroundColor Cyan
playwright install
Assert-Success "playwright install"

Write-Host "Running tests with pytest..." -ForegroundColor Cyan
python -m pytest -v --headless=true
$testExitCode = $LASTEXITCODE

Write-Host "Starting Allure report server..." -ForegroundColor Cyan
allure serve allure-results

# Propagate the test result, not allure serve's - a failing run must still
# show the report, but the script's own exit code should reflect the tests.
exit $testExitCode
