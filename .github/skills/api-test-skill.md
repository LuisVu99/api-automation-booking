# Skill: API Test Case Generation Guidelines

This skill defines the technical rules and logic for converting API specs into detailed CSV test cases using a common checklist.

## 1. Checklist-Driven Generation Logic

When generating test cases for each API endpoint:
1. **Read Checklist First**: Analyze every scenario listed in `common_api_checklist.md`.
2. **Endpoint Mapping**: For every endpoint in the API Doc, apply applicable items from the checklist:
   - **Authentication & Authorization**: Verify token missing, expired token, invalid role/permissions (401/403).
   - **Input Validation**: Missing required fields, null values, empty strings, invalid data types, exceeded max length (400).
   - **Business Logic & Boundaries**: Min/max boundary values, special characters, duplicate records, non-existent IDs (400/404/409).
   - **Happy Path / Success**: Valid payloads, expected status codes (200/201/204), response body structure.
   - **Headers & Media Types**: Unsupported `Content-Type`, missing custom headers.

## 2. CSV Output & Formatting Rules

- **Language**: All text (titles, preconditions, steps, expected results) **MUST be written in ENGLISH**.
- **Template Alignment**: Map content to **100% of the columns** defined in the user's CSV template.
- **CSV Escaping Compliance**:
  - Wrap any cell containing commas (`,`), line breaks (`\n`), or quotes (`"`) inside double quotes (`"`).
  - Escape internal double quotes with double-double quotes (`""`).
- **No Extra Text**: Output ONLY the raw CSV content wrapped in a ` ```csv ` block. Do not include introductory or concluding messages.