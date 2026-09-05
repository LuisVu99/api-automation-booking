# API Automation Framework Template

A modular Python API automation framework built with Pytest, Requests, Pydantic v2, Allure, python-dotenv, and CSV-driven test data.

## Features

- Environment-based configuration with validation
- Reusable Requests session and common diagnostics
- Endpoint classes separated from test logic
- Pydantic v2 response and request models
- CSV data-driven tests with readable case IDs
- Allure request and response attachments
- Generic CSV-driven requests with flexible status, key, and value assertions
- Per-row role authentication using `API_TOKEN_ADMIN`, `API_TOKEN_USER`, and `API_TOKEN_GUEST`
- Session-scoped in-memory token and cookie cache with refresh after HTTP 401
- Response chaining between ordered CSV test cases
- GitHub Actions continuous integration

## Project Layout

- `config`: runtime settings
- `endpoints`: reusable API clients
- `models`: Pydantic request and response models
- `test_data/csv`: data-driven test cases
- `utils`: CSV parsing, response verification, authentication cache, and request chaining
- `tests`: fixtures and test scenarios

## Setup

Use Python 3.11 or newer.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `.env` with the target product URL and credentials or token when required. The default URL points to JSONPlaceholder so the sample tests can run without credentials.

## Run Tests

```bash
pytest
pytest -m smoke
pytest --clean-alluredir --alluredir=allure-results
```

To view the Allure report, install the Allure command-line tool and run:

```bash
allure serve allure-results
```

## CSV Test Cases

The test suite reads `test_data/csv/*.csv`. Add, update, or remove scenarios by editing CSV rows only. The required columns are:

`Execute,case_id,Title,Priority,Role,Method,API URL,Request Body,expected_type,expected_result`

Only rows whose `Execute` value is `yes` (case-insensitive) run. All other values are skipped. `Request Body` contains a JSON object. `expected_type` supports `status_code`, `verify_body_empty`, `verify_type`, `response_time`, `verify_content_type`, `verify_keys`, and `verify_values`:

- `status_code`: `expected_result` is one or more HTTP codes, such as `200` or `200, 201`.
- `verify_keys`: `expected_result` is a comma-separated list of response key paths, such as `id, data.status, data.items[0].name`.
- `verify_values`: `expected_result` is a comma-separated list of `path=value` expressions, such as `data.status=ACTIVE, data.count=2, data.enabled=true`.
- `verify_body_empty`: `expected_result` is `true` or `false`.
- `verify_type`: `expected_result` is a JSON type such as `object`, `array`, `string`, `number`, `boolean`, or `null`.
- `response_time`: `expected_result` is a time comparison such as `<5000ms` or `<=5s`; the measurement uses the HTTP response elapsed time.
- `verify_content_type`: `expected_result` is the expected MIME type, such as `application/json`. The existing `expected_content_type` value is also supported as an alias.

Key paths support dot notation, array indexes, and an optional `$` root prefix. Values are parsed as JSON scalars when possible, so numbers, booleans, and `null` are compared using their native types.

Use a relative path such as `/users/1` or an absolute URL in `API URL`. Set `Role` to `Admin`, `User`, or `Guest`; non-guest roles use the corresponding `API_TOKEN_<ROLE>` environment variable and fall back to `API_TOKEN`. `Guest` sends no authentication token.

When dynamic authentication is required, set `API_USERNAME` and `API_PASSWORD`. A named non-guest role logs in lazily once, caches the returned token and cookies in memory, and reuses them across test cases. The token is sent as the `token` cookie by the current client. Configure `API_AUTH_PATH` when the login endpoint differs from `/auth/login`, and set `API_TOKEN_JSON_PATH` to the token field returned by the login response, such as `access_token` or `data.token`. A `401` response invalidates the cached token, performs one login refresh, and retries the original request once. Requests with no role or with `Guest` do not trigger this flow.

## API Test Case Generator Agent

This repository includes the `gen_api_case` agent for generating CSV-driven API test cases from API documentation.

### Agent Files

- `.github/agents/gen_api_case.agent.md`: defines the four-step generation workflow.
- `.github/skills/api-test-skill.md`: defines endpoint mapping, required coverage, and CSV formatting rules.
- `documents/common_api_checklist.md`: contains the reusable API test checklist.
- `test_data/csv/user_api_cases.csv`: contains the target CSV template and generated cases.

### How to Use

In Copilot Chat, invoke the agent and attach the three required files with `#file` tags:

```text
@gen_api_case #file:booking_document.md #file:user_api_cases.csv #file:common_api_checklist.md
```

Use the workspace-relative paths when the files are not already open or attached:

```text
@gen_api_case #file:documents/booking_document.md #file:test_data/csv/user_api_cases.csv #file:documents/common_api_checklist.md
```

The three inputs are required:

1. API documentation with endpoints, methods, parameters, request bodies, response fields, and status codes.
2. The CSV template whose column structure must be preserved.
3. The common API checklist used to select applicable validation scenarios.

The agent validates the inputs, reads the checklist and API test skill, maps applicable checks to every endpoint, and generates happy-path, validation, authorization, header, boundary, and error cases where relevant. All generated case text is written in English and must match every column in the supplied CSV template.

### Updating the CSV

The agent returns only one `csv` code block. Review the generated rows, then update the target file, normally `test_data/csv/user_api_cases.csv`. Preserve CSV escaping: fields containing commas or quotes must remain enclosed in double quotes, and JSON quotes inside a field must be doubled.

After updating the file, validate its structure and duplicate case IDs before running the tests:

```powershell
python -c "import csv; from pathlib import Path; p=Path('test_data/csv/user_api_cases.csv'); rows=list(csv.DictReader(p.open(newline='', encoding='utf-8-sig'))); assert rows and all(len(r)==10 for r in rows); ids=[r['case_id'] for r in rows]; assert len(ids)==len(set(ids)); print(f'Valid CSV: {len(rows)} cases')"
pytest --clean-alluredir --alluredir=allure-results
```

When adding more cases, keep `case_id` unique and place setup cases before cases that use response chaining placeholders such as `{bookingid}`.

## Request Chaining

CSV cases can use values returned by earlier cases. Add a placeholder in `API URL` or `Request Body` using braces:

```csv
yes,create_booking,Create booking,normal,Admin,POST,/booking,"{""firstname"": ""Luis""}",status_code,200
yes,delete_booking,Delete booking,normal,Admin,DELETE,/booking/{booking_id},,status_code,200
```

If the create response is `{"booking_id": 123}`, the second case sends `DELETE /booking/123`. Nested paths and array indexes are supported:

```text
/booking/{response.data.booking_id}
/users/{response.items[0].id}
```

Placeholders in a JSON request body preserve the original value type when the complete value is a placeholder:

```json
{"booking_id": "{booking_id}", "active": true}
```

The case that creates the value must run before the case that consumes it. The response is available both directly, for example `{booking_id}`, and under the `response` root, for example `{response.data.booking_id}`. Missing placeholders fail the test with a descriptive error.

## Adapting the Template

1. Replace `API_BASE_URL` in `.env`.
2. Add or update CSV rows for new scenarios; no test code changes are needed.
3. Add product-specific endpoint methods or Pydantic models only when application code needs typed workflows outside the generic CSV runner.
4. Add role token environment variables when the target API requires authentication.

Never commit `.env` or real credentials. Keep secrets in the CI secret store and expose them as environment variables.
