#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$testPlan = Join-Path $root "performance/jmeter/user_api_load_test.jmx"
$resultsDir = Join-Path $root "performance/results"
$jtl = Join-Path $resultsDir "results.jtl"
$htmlReport = Join-Path $resultsDir "html-report"

New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null

if (Get-Command jmeter -ErrorAction SilentlyContinue) {
    Write-Host "Running JMeter from local installation..." -ForegroundColor Cyan
    jmeter -n -t $testPlan -l $jtl -e -o $htmlReport
    if ($LASTEXITCODE -ne 0) {
        throw "JMeter run failed with exit code $LASTEXITCODE"
    }
} else {
        Write-Host "JMeter not found locally. Running with Docker image justb4/jmeter:latest..." -ForegroundColor Yellow
        docker run --rm -v "${root}:/work" -w /work justb4/jmeter:latest `
      -n -t performance/jmeter/user_api_load_test.jmx `
      -l performance/results/results.jtl `
      -e -o performance/results/html-report
    if ($LASTEXITCODE -ne 0) {
        throw "Docker-based JMeter run failed with exit code $LASTEXITCODE"
    }
}

Write-Host "Performance run completed." -ForegroundColor Green
Write-Host "JTL: $jtl"
Write-Host "HTML report: $htmlReport"
