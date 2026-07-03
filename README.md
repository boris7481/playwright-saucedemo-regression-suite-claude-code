# Playwright SauceDemo — E2E Test Suite

[![Tests E2E](https://github.com/boris7481/playwright-saucedemo-regression-suite-claude-code/actions/workflows/tests.yml/badge.svg)](https://github.com/boris7481/playwright-saucedemo-regression-suite-claude-code/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.60.0-45ba4b?logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-9.1.1-0A9EDC?logo=pytest&logoColor=white)
![Allure](https://img.shields.io/badge/Reports-Allure-FF6E00?logo=qameta&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Project Overview

This repository contains an end-to-end test suite for the [SauceDemo](https://www.saucedemo.com/) demo site, built with **Playwright (Python)** and **pytest**. The framework follows a complete **Page Object Model** architecture, with centralized test data, continuous integration via **GitHub Actions**, and test reporting via **Allure**.

This is a professional test automation framework, built incrementally over 12 sprints, each validated by an explicit diff and a dedicated commit (see [Sprint history](#sprint-history)).

## Goals

- Demonstrate a professional, readable, and maintainable E2E test architecture for a QA team.
- Showcase Playwright/pytest best practices: Page Object Model, fixtures, targeted parametrization, reporting, CI/CD.
- Serve as a technical reference for test automation.

## Technologies Used

| Tool | Role |
|---|---|
| Python 3.13 | Language |
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [pytest](https://docs.pytest.org/) | Test framework |
| pytest-playwright | Playwright / pytest integration |
| pytest-base-url | `base_url` management |
| pytest-xdist | Parallel test execution |
| [allure-pytest](https://allurereport.org/) | Structured test result generation |
| GitHub Actions | Continuous integration |
| Faker | Data generation (available) |

## Project Architecture

```
tests/  ──uses──▶  fixtures (conftest.py)  ──instantiate──▶  Page Objects  ──drive──▶  Playwright
                                                                    │
test_data/  ◀──used by tests and Page Objects─────────────────────┘
```

Guiding principles:
- **No assertions inside Page Objects** — they expose actions (`login()`, `add_to_cart()`) and state readers (`get_product_prices()`), never verifications. Assertions stay in the tests.
- **No hardcoded strings** in the tests — all data (credentials, products, messages) comes from `test_data/`.
- **Page Objects are injected via pytest fixtures**, never instantiated manually inside a test.

## Repository Structure

```
playwright-saucedemo-regression-suite_bis/
├── .github/workflows/tests.yml   # CI pipeline: runs the test suite on push/PR to main
├── docs/screenshots/                # Allure report screenshot
├── pages/
│   ├── base_page.py                 # Shared behavior (navigation, menu, logout)
│   ├── login_page.py                 # Page Object: login
│   ├── inventory_page.py              # Page Object: product catalog
│   ├── cart_page.py                    # Page Object: shopping cart
│   └── checkout_page.py                 # Page Object: checkout flow
├── test_data/
│   ├── users.py                    # Test credentials
│   ├── products.py                  # Product catalog, prices, sort options
│   ├── checkout_info.py              # Checkout form data
│   └── messages.py                    # Expected business error/success messages
├── tests/
│   ├── test_login.py                # Login scenarios
│   ├── test_inventory.py             # Catalog, sorting
│   ├── test_card.py                   # Shopping cart
│   ├── test_checkout.py                # Checkout flow
│   ├── test_e2e_order.py                # Full end-to-end order flow
│   └── test_logout.py                    # Logout
├── conftest.py                     # pytest fixtures (authentication, Page Objects)
├── pytest.ini                      # pytest configuration (base_url, --headed)
├── requirements.txt                # Pinned Python dependencies
├── .editorconfig                   # Editor conventions
├── .gitignore
├── LICENSE                         # MIT License
└── README.md
```

## Installation

### Prerequisites
- Python 3.13+
- Git

### Creating the virtual environment
```bash
python -m venv .venv
```
Activation:
```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### Installing dependencies
```bash
pip install -r requirements.txt
```

### Installing Playwright browsers
```bash
playwright install chromium
```
> In CI (Linux), the `--with-deps` flag also installs the required system libraries: `playwright install --with-deps chromium` (already configured in the GitHub Actions workflow).

## Test Execution

Run the whole suite (`--headed` by default, see `pytest.ini`):
```bash
pytest
```

### Running a test file
```bash
pytest tests/test_checkout.py
```

### Running a single test
```bash
pytest tests/test_checkout.py::test_checkout_complete
```

### Parametrized tests
```bash
# All cases of a parametrized test
pytest tests/test_checkout.py::test_checkout_required_field

# One specific case, by its id
pytest "tests/test_checkout.py::test_checkout_required_field[missing_first_name]"

# Filtering by keyword
pytest -k "missing_first_name"
```

## Generating Allure Reports

Allure integration is **opt-in** (not enabled by default in `pytest.ini`, to keep `pytest` neutral locally):
```bash
# 1. Run the tests, generating raw results
pytest --alluredir=reports/allure-results

# 2. View the report (requires the allure tool, installed separately from pip)
allure serve reports/allure-results

# — or generate a static HTML report —
allure generate reports/allure-results -o reports/allure-report --clean
```
> The `allure` CLI (Java-based) is installed separately from `allure-pytest`: e.g. `scoop install allure` (Windows), `brew install allure` (macOS).

## Running the GitHub Actions Pipeline

The `.github/workflows/tests.yml` workflow triggers automatically on every `push` or `pull_request` to `main`. It can also be run manually from the **Actions** tab of the repository → **Tests E2E** → **Run workflow**. The badge at the top of this README reflects the status of the latest run.

The pipeline runs the tests on `ubuntu-latest` via `xvfb-run` (to preserve `--headed` mode without touching `pytest.ini`), generates Allure results, captures failures as screenshots, then publishes two downloadable artifacts from the run page: `allure-results` and `playwright-screenshots`.

## Page Object Structure

| Page Object | File | Responsibility |
|---|---|---|
| `BasePage` | `pages/base_page.py` | Cross-cutting behavior: navigation, menu, logout |
| `LoginPage` | `pages/login_page.py` | Login form |
| `InventoryPage` | `pages/inventory_page.py` | Product catalog, sorting, adding to cart |
| `CartPage` | `pages/cart_page.py` | Cart contents, removal, navigation to checkout |
| `CheckoutPage` | `pages/checkout_page.py` | Checkout flow (information, summary, confirmation) |

## Test Data Structure

| File | Content |
|---|---|
| `test_data/users.py` | Credentials (standard, locked-out, invalid user...) |
| `test_data/products.py` | Product names, prices, sort options |
| `test_data/checkout_info.py` | Checkout form data sets |
| `test_data/messages.py` | Expected business error / success messages |

Deliberate choice: plain dictionaries rather than `dataclass`, to stay readable and ready to be reused directly in `pytest.mark.parametrize`.

## Fixtures Used

| Fixture | Scope | Role |
|---|---|---|
| `page` | function (pytest-playwright) | Raw, unauthenticated Playwright page |
| `authenticated_page` | function | Page logged in as the standard user |
| `login_page` | function | `LoginPage` instance bound to `page` |
| `inventory_page` | function | `InventoryPage` instance bound to `authenticated_page` |
| `cart_page` | function | `CartPage` instance bound to `authenticated_page` |
| `checkout_page` | function | `CheckoutPage` instance bound to `authenticated_page` |

## Framework Best Practices

- No hardcoded strings: all data comes from `test_data/`.
- No assertions inside Page Objects — strict separation between actions and verifications.
- Page Objects injected via fixtures, never instantiated manually inside a test.
- `pytest.mark.parametrize` used only when several tests share the exact same behavior — no forced parametrization.
- Reporting and CI are strictly opt-in (`--alluredir`, `--screenshot`): the default local `pytest` behavior has never been changed.
- Every evolution of the framework was validated through an explicit diff before being applied.

## Screenshots

### Allure Report
![Allure Report](docs/screenshots/allure-report.png)

## Sprint History

| Sprint | Content |
|---|---|
| 1-5 | Full Page Object Model setup (`BasePage`, `LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`) |
| 6 | Test data centralization (`test_data/`) |
| 7 | pytest fixtures for Page Object injection |
| 8 | Targeted parametrization with `pytest.mark.parametrize` |
| 9 | Playwright Storage State study (deferred) |
| 10 | Allure Reports integration |
| 11 | GitHub Actions pipeline (CI) |
| 12 | Documentation and repository professionalization |
| 13 | Full documentation internationalization (English) |

## Author

**Author:** Boris Thibaut Tondjua
**GitHub:** [@boris7481](https://github.com/boris7481)

## Future Improvements

- Playwright Storage State to avoid repeated UI logins (deferred in Sprint 9, ready to be implemented).
- Automated Allure report publishing with trend history across CI runs.
- Multi-browser execution (Firefox, WebKit) in addition to Chromium.
- Adding a lint/format tool (ruff, black) with a dedicated CI workflow.
- Configurable environments (staging/production) via an environment variable for `base_url`.

## License

This project is distributed under the MIT License — see the [LICENSE](LICENSE) file.
