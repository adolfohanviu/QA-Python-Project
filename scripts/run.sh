#!/bin/bash

set -e

echo "Setting environment variables..."
export HEADLESS=true
export API_BASE_URL="https://jsonplaceholder.typicode.com"

echo "Installing Playwright browsers..."
playwright install

echo "Running tests with pytest..."
python -m pytest -v --headless=true

echo "Starting Allure report server..."
allure serve allure-results
