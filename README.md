# Playwright Automation Framework (Python)

Comprehensive end-to-end test automation framework built with Python, Pytest, and Playwright. Designed for UI and API testing with Allure reporting, headless execution, and CI/CD integration.

> **Status**: ✅ CI/CD pipelines configured and passing - All Tests, Smoke Tests, Regression Tests

## Features

- **Playwright** - Modern cross-browser automation with async/await support
- **Pytest** - Flexible and scalable test framework with powerful fixtures
- **Async Tests** - Native async test support via pytest-asyncio
- **API Testing** - REST API testing with requests library and fixtures
- **API Mocking** - WireMock offline mode for deterministic contract tests
- **Allure Reporting** - HTML reports with steps, logs, and screenshots
- **Headless Mode** - Environment- or CLI-controlled browser execution
- **GitHub Actions CI/CD** - Automated test execution on push/PR with report publishing
- **Page Object Model** - Maintainable UI test structure
- **Test Data Fixtures** - JSON-based test data management
- **Multi-browser Support** - Chromium, Firefox, WebKit
- **Docker** - Containerized testing with multi-stage builds and compose
- **Kubernetes** - Production-grade cluster deployment with RBAC and ConfigMaps
- **Logging** - Comprehensive logging with CLI and file output

## Project Structure

```
tests/
├── api/                    # API tests and client
│   ├── api_client.py      # REST API wrapper
│   └── test_user_api.py   # API test cases
├── pageobjects/           # Page Object Model classes
│   ├── base_page.py       # Base page with common functions
│   └── login_page.py      # Login page object
├── fixtures/              # Test data fixtures
│   └── api_users.json     # API test data
├── mocks/                 # WireMock mappings and responses
│   ├── mappings/           # Request/response mappings
│   └── __files/            # Mock response bodies
├── utils/                 # Utilities and helpers
│   └── config.py          # Configuration management
├── features/              # Gherkin feature files (future)
├── screenshots/           # Failure screenshots
├── conftest.py            # Pytest fixtures and hooks
└── test_*.py              # Test files

.github/workflows/         # GitHub Actions CI/CD
├── all-tests.yml         # All tests workflow
├── smoke-tests.yml       # Smoke tests (daily schedule)
├── regression-tests.yml  # Regression tests (daily schedule)
└── docker-build.yml      # Docker build and push workflow

scripts/                   # Helper scripts
├── run.sh               # Bash wrapper (macOS/Linux)
└── run.ps1              # PowerShell wrapper (Windows)

k8s/                      # Kubernetes manifests
├── namespace.yaml        # QA automation namespace
├── configmap.yaml        # Configuration management
├── rbac.yaml             # Role-based access control
├── job.yaml              # Test execution job
└── deployment.yaml       # Allure report UI deployment

Docker/                    # Container configuration
├── Dockerfile            # Multi-stage build
├── docker-compose.yml    # Local development compose
└── .dockerignore         # Build context exclusions

config/                    # Configuration files
requirements.txt           # Python dependencies
pytest.ini                # Pytest configuration
README.md                 # This file
```

## Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **Git**

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/adolfohanviu/QA-Python-Project.git
cd QA-Python-Project
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers
```bash
playwright install
```

## Running Tests

### Run all tests
```bash
pytest -v
```

### Run by marker
```bash
pytest -m smoke -v        # Smoke tests only
pytest -m regression -v   # Regression tests only
pytest -m api -v         # API tests only
pytest -m ui -v          # UI tests only
pytest -m contract -v    # API contract tests only
```

### Tagging strategy (recommended)

```bash
# Only smoke tests
pytest -m smoke -v

# Regression without contract tests
pytest -m "regression and not contract" -v

# Contract tests (API + mocks)
pytest -m contract -v
```

### Run with environment variables
```bash
HEADLESS=true BASE_URL=https://www.saucedemo.com pytest -v
```

### Run single test file
```bash
pytest tests/api/test_user_api.py -v
```

### Run with headless mode enabled
```bash
pytest -v --headless=true
```

### Run in headed mode
```bash
pytest -v --headless=false
```

## One-Command Execution (Recommended)

**Windows (PowerShell):**
```powershell
.\scripts\run.ps1
```

**macOS/Linux (Bash):**
```bash
bash scripts/run.sh
```

This automatically:
- Sets HEADLESS=true
- Installs Playwright browsers
- Runs all tests
- Generates Allure report
- Serves report on http://localhost:4040

## Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `HEADLESS` | true | Run browser in headless mode |
| `BASE_URL` | https://www.saucedemo.com | UI test target URL |
| `API_BASE_URL` | https://jsonplaceholder.typicode.com | API base endpoint |
| `BROWSER_TYPE` | chromium | Browser engine (chromium/firefox/webkit) |
| `TIMEOUT` | 30000 | Action timeout in milliseconds |
| `LOG_LEVEL` | INFO | Logging level |

### Configuration File

Edit `tests/utils/config.py` to customize framework behavior:

```python
config = Config()
# base_url: UI test target
# api_base_url: API endpoint
# headless: headless mode flag
# timeout: default action timeout
```

## Test Data & Fixtures

### API Fixtures

Test data is managed in `tests/fixtures/api_users.json`:

```json
{
  "userBasic": {
    "name": "Automation User",
    "email": "automation@test.com"
  },
  "userUpdate": {
    "email": "updated@test.com"
  }
}
```

### Loading Fixtures in Tests

```python
from tests.utils.config import config

fixture_data = config.load_fixture("userBasic")
response = self.client.post("/users", fixture_data)
```

## Docker & Containerization

### Build Docker Image

```bash
# Build the image
docker build -t qa-python-tests:latest .

# Run tests in container
docker run --rm qa-python-tests:latest pytest -v
```

### Docker Compose (Recommended)

```bash
# Run all services (tests + Allure reporting UI)
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f test-runner

# Cleanup
docker-compose down -v
```

This starts:
- **test-runner**: Executes all tests
- **allure-ui**: Report viewer on http://localhost:4040

### Environment Variables in Docker

```bash
docker run --rm \
  -e HEADLESS=true \
  -e BASE_URL=https://www.saucedemo.com \
  -e API_BASE_URL=https://jsonplaceholder.typicode.com \
  qa-python-tests:latest pytest -v
```

### API Mocking (Offline Mode)

Run API tests against local WireMock for deterministic, offline runs:

```bash
# Start WireMock + tests (offline mode)
API_BASE_URL=http://wiremock:8080 docker-compose --profile mock up
```

Local WireMock only:

```bash
docker run --rm -p 8081:8080 \
  -v %cd%/mocks:/home/wiremock \
  wiremock/wiremock:2.35.0

# Run tests pointing at local mock
API_BASE_URL=http://localhost:8081 pytest -m contract -v
```

## Kubernetes Deployment

Deploy tests and monitoring infrastructure to Kubernetes cluster:

### Prerequisites
- Kubernetes cluster (v1.20+)
- kubectl configured
- Docker image pushed to registry

### Deploy Resources

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create configuration
kubectl apply -f k8s/configmap.yaml

# Setup RBAC
kubectl apply -f k8s/rbac.yaml

# Deploy Allure report UI
kubectl apply -f k8s/deployment.yaml

# Run test job
kubectl apply -f k8s/job.yaml
```

### Monitor Test Execution

```bash
# List running jobs
kubectl get jobs -n qa-automation

# View test pod logs
kubectl logs -n qa-automation -l app=qa-test-runner

# Get test results
kubectl exec -n qa-automation <pod-name> -- cat /app/allure-results/*
```

### Access Allure UI

```bash
# Port forward to local machine
kubectl port-forward -n qa-automation svc/allure-report-service 4040:80

# Open browser: http://localhost:4040
```

## Allure Reports

### Generate and view report locally
```bash
pytest -v
allure serve allure-results
```

Opens report on http://localhost:4040

### Report includes:
- Test execution timeline
- Pass/fail breakdown
- Failure screenshots
- Step-by-step logs
- Request/response details

## API Testing

### Using the APIClient

```python
from tests.api.api_client import APIClient

client = APIClient()

# GET request
response = client.get("/users")

# POST with data
response = client.post("/users", {"name": "John", "email": "john@test.com"})

# GET JSON response
data = response.get_json()

# Check status
assert client.get_status_code() == 200
```

## Page Object Model (POM)

### Creating page objects

```python
from tests.pageobjects.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = "[data-test='username']"
    
    async def login(self, username: str, password: str):
        await self.fill_text(self.USERNAME_INPUT, username)
        await self.click("[data-test='login-button']")
```

### Using page objects in tests

```python
async def test_login(page):
    login = LoginPage(page)
    await login.goto(config.base_url)
    await login.login("user", "password")
```

## Parallel Execution

Run tests in parallel with pytest-xdist:

```bash
pytest -n auto -v    # Auto-detect number of cores
pytest -n 4 -v       # Use 4 workers
```

## CI/CD Integration

### GitHub Actions Workflows

Three automated workflows are configured:

**1. All Tests** - Runs on push/PR to main
```bash
pytest -v
```

**2. Smoke Tests** - Scheduled daily at 6 AM
```bash
pytest -m smoke -v
```

**3. Regression Tests** - Scheduled daily at 10 PM
```bash
pytest -m regression -v
```

All workflows:
- Install Python 3.11
- Install Playwright browsers
- Run tests with `HEADLESS=true`
- Generate and publish Allure reports to GitHub Pages (Allure history dashboard)

### Test Dashboard
Allure reports include historical trend charts published to GitHub Pages, providing a lightweight dashboard for tracking test health over time.

## Logging

Logs are displayed in console and can be configured:

```python
# In pytest.ini
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
```

### Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Best Practices

- ✅ Use Page Object Model for UI tests
- ✅ Load test data from fixtures, not inline
- ✅ Mark tests with `@pytest.mark.smoke`, `@pytest.mark.regression`
- ✅ Use async/await for cleaner test code
- ✅ Capture failures with screenshots
- ✅ Use meaningful assertion messages
- ✅ Keep tests independent and idempotent
- ✅ Use fixtures for setup/teardown

## Troubleshooting

### Playwright browsers not installed
```bash
playwright install
```

### Tests timeout
Increase timeout in config or per test:
```python
await page.goto(url, timeout=60000)  # 60 seconds
```

### Allure report not generating
```bash
pip install allure-pytest
pytest --alluredir=allure-results
```

## Author

Adolfo Han - Senior SDET/QA Engineer
