# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BDD test automation framework (Python) combining **Behave + Playwright + Google Gemini AI** for intelligent, self-healing, visually-aware E2E testing. Tests run on Windows with a `.venv` virtual environment (Python 3.13).

## Commands

```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run all @Regression tests with Allure reporting
python -m behave --format allure_behave.formatter:AllureFormatter -o allure-results --tags=@Regression

# Run a single feature
python -m behave features/registration.feature

# Run by tag
python -m behave --tags=@Login
python -m behave --tags=@VisualTesting
python -m behave --tags=@AI1
python -m behave --tags=@MCP

# Run API tests (pytest, requires local server on localhost:8080)
python -m pytest features/apitests/test_playwright_API.py -v

# Generate Allure report
allure generate allure-results -o allure-report --clean

# Full regression pipeline (runs tests, generates report, publishes to GitHub Pages, sends email)
run_regression_publish.bat
```

## Architecture

### Behave BDD Layer
- **`features/*.feature`** — Gherkin scenarios tagged with `@Regression`, `@Login`, `@System`, `@VisualTesting`, `@AI1`, `@AI2`, `@AI3`, `@MCP`, `@Self_healing`
- **`features/steps/*_step.py`** — Step definitions. Each step file instantiates page objects with `context.page` and `context.scenario_logger`
- **`features/environment.py`** — Behave hooks (`before_all`, `before_scenario`, `after_step`, `after_scenario`, `after_all`). Manages Playwright browser lifecycle, per-scenario logging, Allure screenshot-on-failure, and API request context

### Page Object Model
- **`features/pageobjects/BasePage.py`** — All UI interactions (click, type, select, get_text, waits). Locators are resolved at runtime from `ConfigurationData/conf.ini` via `configReader.readConfig("locators", key)`. Every action is wrapped in `allure.step()` and logged
- **`features/pageobjects/RegistrationPage.py`** — Extends BasePage for Way2Automation registration and SwagLabs login flows

### Locator Resolution Pattern
Locators are **not hardcoded** in page objects. They live in `ConfigurationData/conf.ini` under `[locators]` and are referenced by key name (e.g., `"username_swagLabs_XPATH"`). When adding new page interactions, add the locator to `conf.ini` and reference the key in the page object.

### AI / Generative AI Layer (`ai/`)
- **`ai/genAI_gemini.py`** — Three Gemini functions: `generate_scenarios_asserts` (generates test scenarios from prompt), `validate_text_with_llm` (semantic text validation returning PASS/FAIL dict), `suggest_alternative_locators` (self-healing: suggests alternative selectors with confidence scores)
- **`ai/mcp_client.py`** — Emulated MCP (Model Context Protocol): `mcp_decide_tool` routes prompts to the right tool, `run_mcp` orchestrates tool selection and execution
- **`ai/mcp_tools.py`** — Tool registry with JSON-schema definitions for MCP routing
- **`ai/openAIAgentTest.py`** — Standalone `browser-use` Agent experiment (not part of Behave suite)
- Requires `GOOGLE_API_KEY` environment variable for all Gemini calls

### Configuration & Utilities
- **`ConfigurationData/conf.ini`** — INI file with sections: `[urls]`, `[credentials]`, `[browser]`, `[locators]`
- **`Utilities/configReader.py`** — Reads `conf.ini` via `readConfig(section, key)`
- **`Utilities/logUtil.py`** — Logger class writing to `Logs/run_<timestamp>.log` with feature/scenario context in each line
- **`Utilities/image_compare.py`** — PIL-based visual diff (`compare_images`) used by visual testing scenarios
- **`Utilities/email_sender.py`** — Gmail SMTP notification with log attachment (uses env vars `EMAIL_SENDER`, `EMAIL_RECEIVER`, `EMAIL_APP_PASSWORD`)
- **`Utilities/allure_report_helper.py`** — Zips allure-results for portability

### Visual Testing Flow
Screenshots are stored in `visual_baseline/` (reference), `visual_actual/` (current run), and `visual_diff/` (differences). On first run, the actual screenshot becomes the baseline automatically.

### CI / Reporting Pipeline
`run_regression_publish.bat` runs the full 7-step pipeline: activate venv, clean allure, run `@Regression` tests, generate report, publish to GitHub Pages (`automation-reports` sibling repo), send email notification, and report final status.

## Environment Variables

| Variable | Purpose |
|---|---|
| `GOOGLE_API_KEY` | Google Gemini API access (required for @AI and @MCP tests) |
| `EMAIL_SENDER` | Gmail sender address (optional, has fallback) |
| `EMAIL_RECEIVER` | Gmail receiver address (optional, has fallback) |
| `EMAIL_APP_PASSWORD` | Gmail app password (optional, falls back to conf.ini) |

## Key Conventions

- Browser type is configured in `conf.ini` `[browser]` section (chrome, edge, firefox, safari). Tests run **headed** (headless=False)
- All Behave scenarios get a fresh browser instance and API request context via `before_scenario`/`after_scenario`
- The `context.scenario_logger` (LoggerAdapter) must be passed when instantiating any page object
- API tests under `features/apitests/` use pytest, not Behave, and require a local server at `localhost:8080`
