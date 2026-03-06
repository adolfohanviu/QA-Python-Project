#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_PLAN="$ROOT_DIR/performance/jmeter/user_api_load_test.jmx"
RESULTS_DIR="$ROOT_DIR/performance/results"
JTL="$RESULTS_DIR/results.jtl"
HTML_REPORT="$RESULTS_DIR/html-report"

mkdir -p "$RESULTS_DIR"

if command -v jmeter >/dev/null 2>&1; then
  echo "Running JMeter from local installation..."
  jmeter -n -t "$TEST_PLAN" -l "$JTL" -e -o "$HTML_REPORT"
else
  echo "JMeter not found locally. Running with Docker image justb4/jmeter:latest..."
  docker run --rm -v "$ROOT_DIR:/work" -w /work justb4/jmeter:latest \
    -n -t performance/jmeter/user_api_load_test.jmx \
    -l performance/results/results.jtl \
    -e -o performance/results/html-report
fi

echo "Performance run completed."
echo "JTL: $JTL"
echo "HTML report: $HTML_REPORT"
