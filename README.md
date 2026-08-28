# Senior QA Platform Engineering Portfolio - Playwright Python Framework

Comprehensive QA platform engineering project built with Python, Pytest, and Playwright, covering UI/API automation, BDD scenarios, CI quality gates (flake8 and pylint), performance testing with JMeter, Docker/Kubernetes validation flows, and LGTM observability (Loki, Grafana, Tempo, Prometheus) for timestamp-correlated root-cause analysis.

> **Status**: ✅ End-to-end portfolio implementation active - UI/API automation, BDD, Quality Gates, Performance, Docker/K8s validation, and LGTM observability

[![Quality Gates](https://github.com/adolfohanviu/python-qa-platform-framework/actions/workflows/quality-gates.yml/badge.svg)](https://github.com/adolfohanviu/python-qa-platform-framework/actions/workflows/quality-gates.yml)

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

## Senior QA Platform Engineer Stack

- **Core Framework Architecture** - three-layer Python/Pytest design (utilities, fixtures, tests)
- **Automation & Validation** - fast REST API suites and BDD with Cucumber/Gherkin + `pytest-bdd`
- **Resilience Testing** - retry/backoff and timeout handling verified against fault-injected WireMock scenarios (502/503/504, connection drops, slow responses) - see [Resilience testing](#resilience-testing-fault-injection) below
- **AI-Assisted QA Workflows** - Claude Code skills for failure triage and BDD scaffolding, an LLM-backed CI failure-triage step, and a versioned, injection-aware prompt template - see [AI-Assisted QA Engineering](#ai-assisted-qa-engineering) below
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
├── features/              # Gherkin feature files (login.feature, user_api.feature)
├── screenshots/           # Failure screenshots
├── unit/                  # Unit tests for AI triage logic (no browser/network)
│   └── test_ai_failure_triage.py
├── conftest.py            # Pytest fixtures and hooks
└── test_*.py              # Test files

AGENTS.md                  # Canonical agent instructions (setup, conventions, AI workflows)
CLAUDE.md                  # Claude Code-specific pointers on top of AGENTS.md
.claude/skills/             # Project-local Claude Code skills
├── flaky-test-triage/     # Investigate a failing/flaky test
└── bdd-scenario-scaffold/ # Scaffold a new BDD scenario

prompts/                    # Versioned LLM prompt templates
└── failure_triage.md      # Shared by the skill and the CI triage script

.github/workflows/         # GitHub Actions CI/CD
├── all-tests.yml         # All tests workflow (+ AI failure triage on failure)
├── smoke-tests.yml       # Smoke tests (daily schedule)
├── regression-tests.yml  # Regression tests (daily schedule)
├── docker-build.yml      # Docker build and test
├── quality-gates.yml     # flake8 + pylint + API gate + AI triage unit tests
└── performance-tests.yml # JMeter performance workflow

performance/               # Performance test assets
└── jmeter/
  └── user_api_load_test.jmx  # JMeter load plan

mocks/                    # WireMock mappings and responses
├── mappings/             # Request/response mappings
└── __files/              # Mock response bodies

scripts/                   # Helper scripts
├── ai_failure_triage.py # LLM-backed CI failure triage (see AI-Assisted QA Engineering)
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

k8s/                      # Kubernetes manifests
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
git clone https://github.com/adolfohanviu/python-qa-platform-framework.git
cd python-qa-platform-framework
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

### Resilience testing (fault injection)

`APIClient.get()` retries on `502`/`503`/`504` and on connection/read timeouts (2 retries,
exponential backoff), emitting an `api_retry` observability event per attempt so a retry
storm is visible in the same trace as the request it belongs to. POST/PUT/DELETE don't
retry automatically - this API has no idempotency key, so blindly replaying a write could
double-submit it.

This can't be exercised against the real jsonplaceholder API (it doesn't fail on demand),
so `tests/api/test_resilience.py` runs against the WireMock mock instead, using
scenario-based mappings under `mocks/mappings/` (`flaky-users` fails twice then recovers,
`dropped-users` resets the connection once then recovers, `broken-users` always fails,
`slow-users` delays past the client timeout):

```bash
docker compose --profile mock up -d wiremock
pytest -m "resilience" -v
```

Skips cleanly (not a failure) if WireMock isn't running - it's a hard gate in
`quality-gates.yml`, which starts the mock service itself, but not part of the default
`pytest -v` run.

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

The observability stack (`docker-compose.observability.yml`) and the containerized test
runner (`docker-compose.yml`) are two independent Docker networks - this workflow runs
`pytest` directly on the host against the containerized LGTM stack's published ports
(`localhost:4318` etc.), it does not run the test-runner container and the LGTM stack
together. Running `docker-compose up` (test-runner) at the same time as the observability
stack will not produce traces, since the test-runner container can't reach `tempo` by
`localhost`.

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

## AI-Assisted QA Engineering

This project treats AI usage as reviewable engineering, not a marketing bullet - every claim below points at a real file.

| What | Where | Kind |
|---|---|---|
| Root-cause triage for a failing/flaky test | `.claude/skills/flaky-test-triage/SKILL.md` | Claude Code skill (local, interactive) |
| BDD scenario scaffolding | `.claude/skills/bdd-scenario-scaffold/SKILL.md` | Claude Code skill (local, interactive) |
| CI failure triage | `scripts/ai_failure_triage.py` | Runs in CI (`all-tests.yml`), calls the Claude API |
| Shared, versioned prompt | `prompts/failure_triage.md` | Single source of truth for both the skill and the CI script |
| Repo-wide agent instructions | `AGENTS.md` / `CLAUDE.md` | Setup, conventions, and this table, kept current |

### How the CI triage step works

On a failed `pytest` run in `all-tests.yml`, a step gated on `if: failure()` runs `scripts/ai_failure_triage.py`, which:

1. Parses the JUnit XML report for failed/errored tests (capped at `TRIAGE_MAX_FAILURES`, default 5, to bound cost).
2. Correlates each failure with matching JSON events from `logs/qa-tests.log` when observability was enabled for the run.
3. Sends each failure to Claude (`claude-opus-5` by default, override with `TRIAGE_MODEL`) using the prompt in `prompts/failure_triage.md`, and validates the JSON response against a Pydantic schema, retrying once on malformed output.
4. Writes the result to the GitHub Actions step summary, `triage-report.md`, and (on failure) an uploaded `ai-triage-report` artifact.

It never fails the build - triage is diagnostic, not a gate - and skips cleanly, without erroring, when `ANTHROPIC_API_KEY` isn't available (the normal case for a pull request from a fork, since GitHub doesn't expose repo secrets there).

### Prompt-injection awareness

Test failures can contain attacker-controlled content - a scraped page, an API response body. `prompts/failure_triage.md` fences all captured evidence inside `<test_failure>`/`<observability_events>` tags with an explicit instruction never to treat their contents as commands. `tests/unit/test_ai_failure_triage.py` covers the parsing and prompt-building logic (no network calls) so this code is held to the same bar as the rest of the framework.

### Enabling it

Add an `ANTHROPIC_API_KEY` secret to the repository (Settings -> Secrets and variables -> Actions) to turn the CI step on. Locally, the two skills above need no key - they run inside your own Claude Code session.

## CI/CD Integration

### GitHub Actions Workflows

Six automated workflows are configured:

**1. All Tests** - Runs on push/PR to main, triages failures with Claude when they occur
```bash
pytest -v --junitxml=test-results.xml
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
flake8 tests scripts
pylint tests/api tests/utils tests/steps scripts --disable=R,C --fail-under=8.5
pytest -m "api" -v
pytest -m "unit" -v
docker compose --profile mock up -d wiremock && pytest -m "resilience" -v
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

## Verification Evidence (historical snapshot, 2026-03-06)

This is a point-in-time local validation from an earlier commit, kept as a worked example of
what a full local run looks like - it is not regenerated on every change and does not describe
the current `main`. For the current state, check the Quality Gates badge above or the
[Actions tab](https://github.com/adolfohanviu/python-qa-platform-framework/actions).

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
