#!/bin/bash

set -e

echo "Setting environment variables..."
export HEADLESS=true
export API_BASE_URL="https://jsonplaceholder.typicode.com"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install

echo "Running tests with pytest..."
set +e
python -m pytest -v --headless=true
test_exit_code=$?
set -e

echo "Starting Allure report server..."
allure serve allure-results

# Propagate the test result, not allure serve's - a failing run must still
# show the report, but the script's own exit code should reflect the tests.
exit "$test_exit_code"
