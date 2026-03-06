# Playwright Automation Framework (Python)

Comprehensive end-to-end test automation framework built with Python, Pytest, and Playwright. Designed for UI and API testing with Allure reporting, headless execution, and CI/CD integration.

> **Status**: ✅ CI/CD pipelines configured and passing - All Tests, Smoke Tests, Regression Tests

[![Quality Gates](https://github.com/adolfohanviu/playwright-python-automation-framework/actions/workflows/quality-gates.yml/badge.svg)](https://github.com/adolfohanviu/playwright-python-automation-framework/actions/workflows/quality-gates.yml)

## Features

- **Playwright** - Modern cross-browser automation with async/await support
- **Pytest** - Flexible and scalable test framework with powerful fixtures
- **Async Tests** - Native async test support via pytest-asyncio
- **API Testing** - REST API testing with requests library and fixtures
- **Allure Reporting** - HTML reports with steps, logs, and screenshots
- **Headless Mode** - Environment- or CLI-controlled browser execution
- **GitHub Actions CI/CD** - Automated test execution on push/PR with artifacts
- **Page Object Model** - Maintainable, scalable UI test structure
- **Test Data Fixtures** - JSON-based test data management
- **Multi-browser Support** - Chromium, Firefox, WebKit
- **Comprehensive Logging** - Structured logging with CLI and file output
- **Docker Support** - Containerized testing with compose
- **Kubernetes Ready** - Production deployment manifests included

## Senior QA Platform Engineer Stack (Indra ATM)

Tech stack used in production at **Indra ATM (May 2024 - Mar 2025)** and reflected in this portfolio direction:

- **Core Framework Architecture** - three-layer Python/Pytest design (utilities, fixtures, tests)
- **Automation & Validation** - fast REST API suites and BDD with Cucumber/Gherkin + `pytest-bdd`
- **AI-Assisted QA Workflows** - state-machine coverage generation, API exploration, CI failure pattern analysis, secure prompting practices
- **Quality Gates** - flake8 + PEP 8 checks in Buildbot, Pylint feedback in VS Code
- **Performance Engineering** - JMeter test execution with Grafana trend analysis
- **Platform Validation** - Docker and Kubernetes deployment checks automated as part of QA flows
- **Observability** - LGTM stack (Loki, Grafana, Tempo, Prometheus) for timestamp-correlated root-cause analysis

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
├── docker-build.yml      # Docker build and test
├── quality-gates.yml     # flake8 + pylint + API gate
└── performance-tests.yml # JMeter performance workflow

performance/               # Performance test assets
└── jmeter/
  └── user_api_load_test.jmx  # JMeter load plan

mocks/                    # WireMock mappings and responses
├── mappings/             # Request/response mappings
└── __files/              # Mock response bodies

scripts/                   # Helper scripts
├── run.sh               # Bash wrapper (macOS/Linux)
├── run.ps1              # PowerShell wrapper (Windows)
├── run-performance.sh   # JMeter performance runner (macOS/Linux)
├── run-performance.ps1  # JMeter performance runner (Windows)
├── run-observability.sh # Start LGTM stack (macOS/Linux)
├── run-observability.ps1# Start LGTM stack (Windows)
├── stop-observability.sh # Stop LGTM stack (macOS/Linux)
└── stop-observability.ps1# Stop LGTM stack (Windows)

observability/             # LGTM stack configuration
├── loki/                  # Loki config
├── promtail/              # Promtail log scraping config
├── tempo/                 # Tempo tracing config
├── prometheus/            # Prometheus scrape config
└── grafana/               # Grafana datasource provisioning

Docker/                    # Container configuration
├── Dockerfile            # Multi-stage build
└── docker-compose.yml    # Local development compose

k8s/                      # Kubernetes manifests (future)
├── namespace.yaml        # QA automation namespace
├── configmap.yaml        # Configuration management
├── rbac.yaml             # Role-based access control
├── job.yaml              # Test execution job
└── deployment.yaml       # Allure report UI deployment

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
git clone https://github.com/adolfohanviu/playwright-python-automation-framework.git
cd playwright-python-automation-framework
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
pytest -m bdd -v         # BDD scenarios only
```

### Run BDD scenarios directly
```bash
pytest tests/steps/test_user_api_bdd.py -v
pytest tests/steps/test_login_bdd.py -v
```

### Tagging strategy (recommended)

```bash
# Only smoke tests
pytest -m smoke -v

# Regression without contract tests
pytest -m "regression and not contract" -v
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

## Performance Testing (JMeter)

Run JMeter performance tests with provided scripts:

```powershell
.\scripts\run-performance.ps1
```

```bash
bash scripts/run-performance.sh
```

Requirements for these scripts: local `jmeter` installed or Docker daemon running.

## Observability (LGTM)

Start observability stack:

```powershell
.\scripts\run-observability.ps1
```

```bash
bash scripts/run-observability.sh
```

Run tests with observability enabled (logs + traces):

```powershell
$env:OBSERVABILITY_ENABLED="true"
$env:OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
pytest -m "api or bdd" -v
```

```bash
OBSERVABILITY_ENABLED=true OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 pytest -m "api or bdd" -v
```

Stop observability stack:

```powershell
.\scripts\stop-observability.ps1
```

```bash
bash scripts/stop-observability.sh
```

Default endpoints:
- Grafana: `http://localhost:3000` (`admin/admin`)
- Loki: `http://localhost:3100`
- Tempo: `http://localhost:3200`
- Prometheus: `http://localhost:9090`

Log output file for Loki scraping:
- `logs/qa-tests.log`

Outputs are generated under `performance/results/`:
- `results.jtl` (raw execution metrics)
- `html-report/` (visual summary report)

## CI/CD Integration

### GitHub Actions Workflows

Six automated workflows are configured:

**1. All Tests** - Runs on push/PR to main
```bash
pytest -v
```

**2. Smoke Tests** - Scheduled daily at 6 AM + manual trigger
```bash
pytest -m smoke -v
```

**3. Regression Tests** - Scheduled daily at 10 PM + manual trigger
```bash
pytest -m regression -v
```

**4. Docker Build & Test** - Runs on push/PR to main
```bash
docker build && docker run pytest -v
```

**5. Quality Gates** - Runs on push/PR to main + manual trigger
```bash
flake8 tests
pylint tests/api tests/utils tests/steps --disable=R,C --fail-under=8.5
pytest -m "api" -v
```

**6. Performance Tests** - Weekly schedule + manual trigger
```bash
jmeter -n -t performance/jmeter/user_api_load_test.jmx -l performance/results/results.jtl
```

All workflows:
- Install Python 3.11
- Install Playwright browsers
- Run tests with `HEADLESS=true`
- Generate Allure reports
- Upload artifacts with 30-day retention

## Verification Evidence (Mar 6, 2026)

Local validation executed for the portfolio implementation:

- `pytest -m "api or bdd" -v` -> `8 passed, 2 deselected`
- `OBSERVABILITY_ENABLED=true OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 pytest -m "api or bdd" -v` -> `8 passed, 2 deselected`
- `flake8 tests` -> passed
- `pylint tests/api tests/utils tests/steps --disable=R,C --fail-under=8.5` -> `10.00/10` (pass threshold)
- `scripts/run-performance.ps1` -> passed via Docker fallback (`justb4/jmeter:latest`), generated:
  - `performance/results/results.jtl`
  - `performance/results/html-report/`
- Observability evidence generated in `logs/qa-tests.log` with timestamped JSON events (`test_start`, `api_request`, `test_end`).

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
