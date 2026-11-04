# Automation Exercise Test Suite

An automation framework covering **UI** and **API** test cases for the [Automation Exercise](https://automationexercise.com) website. It was created for review purposes.

## Tech Stack

| Area | Tool |
|---|---|
| Language | Python 3.12 |
| Test runner | pytest |
| UI automation | Selenium WebDriver |
| API automation | requests |
| Reporting | pytest-html (local and CI), ReportPortal (local only) |
| CI/CD | GitHub Actions |

## Features

- UI test cases using Selenium and API test cases using the `requests` library
- Runs on **Chrome, Firefox, and Edge**, selected with the `--browser` option
- Markers to separate and filter tests: `smoke`, `ui`, and `api`
- Self-contained **HTML report** generated on both local and CI runs
- **Screenshots captured automatically on failure** and attached to the HTML report
- **ReportPortal integration** for detailed reporting on local runs
- GitHub Actions pipeline that uploads the HTML report and failure screenshots as artifacts

## Project Structure

```text
<project-root>/
├── .github/workflows/ci.yml   # GitHub Actions pipeline
├── tests/
│   ├── ui/                    # Selenium UI tests
│   └── api/                   # requests API tests
├── pages/                     # Page objects (if used)
├── conftest.py                # Fixtures, CLI options, failure-screenshot hook
├── pytest.ini                 # Default pytest options and markers
├── requirements.txt
└── README.md
```
## Prerequisites

- Python 3.12 or later
- At least one of Chrome, Firefox, or Edge installed
- (Optional) A running ReportPortal instance for local reporting

Selenium 4.6 and later downloads the matching browser driver automatically, so no manual driver setup is needed.

## Setup

```bash
git clone <repository-url>
cd <project-folder>

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Running the Tests

Run everything with the defaults from `pytest.ini`:

```bash
pytest
```

Choose a browser:

```bash
pytest --browser=chrome
pytest --browser=firefox
pytest --browser=edge
```

Run by marker:

```bash
pytest -m smoke
pytest -m ui
pytest -m api
pytest -m "ui and smoke"
```

Run a single file or test:

```bash
pytest tests/ui/test_login.py
pytest tests/ui/test_login.py::test_valid_login
```

### Headless mode

Headless is **enabled by default** through `pytest.ini`, so the suite works on machines with no display, such as CI. To watch the browser locally, override it:

```bash
pytest --headless=false
```

### ReportPortal (local only)

ReportPortal is **not** enabled in `pytest.ini`, because the server runs on my local machine and isn't reachable from GitHub-hosted runners. To send results to it, add `--reportportal`:

```bash
pytest --reportportal
```

Set the API key through an environment variable and never commit it:

```bash
export RP_API_KEY=<your-api-key>        # Windows PowerShell: $env:RP_API_KEY="<your-api-key>"
```

The endpoint, project, and launch name are configured in `pytest.ini` or passed with `-o`, for example `-o rp_endpoint=http://localhost:8080`.

## Reports and Screenshots

| Output | Location |
|---|---|
| HTML report | `reports/report.html` (a single, self-contained file) |
| Failure screenshots | `screenshots/` (also embedded in the HTML report) |

Open the HTML report in a browser and click a failed test row to see its screenshot.

## Configuration Summary

| Setting | Local run | CI run |
|---|---|---|
| Headless | Off (overridden in the IDE run configuration) | On (default from `pytest.ini`) |
| ReportPortal | On (`--reportportal`) | Off |
| HTML report | Yes | Yes (uploaded as an artifact) |
| Failure screenshots | Yes | Yes (uploaded as an artifact) |

## Continuous Integration

The workflow in `.github/workflows/ci.yml` runs on pushes and pull requests to `main`. It can also be started manually from the **Actions** tab, where you choose the browser.

After a run, open the workflow run page and download the **test-reports** and **failure-screenshots** artifacts from the *Artifacts* section.

## Markers

| Marker | Purpose |
|---|---|
| `smoke` | Quick sanity checks |
| `ui` | Selenium browser tests |
| `api` | REST API tests using `requests` |

## Notes

- The target site is a public practice website, so occasional slowness or ads can affect UI tests.
- Secrets such as the ReportPortal API key must never be committed. Use environment variables locally and GitHub Secrets in CI.