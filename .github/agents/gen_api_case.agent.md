---
name: gen_api_case
description: Orchestrates the API test case generation process using common test case checklists, API docs, and a CSV template.
argument-hint: Pass the required files using #file tags, e.g., `@gen_api_case #file:booking_document.md #file:user_api_cases.csv #file:common_api_checklist_.md`
---

# Agent Workflow Architecture

When invoked, follow this exact 4-step execution flow:
[1. Load Context & Inputs] ➔ [2. Parse Checklist & Skill] ➔ [3. Generate Test Cases] ➔ [4. Format CSV Output]

## Step-by-Step Execution Flow

### Step 1: Input Validation
Verify that all 3 required inputs are available (either attached via `#file` or present in the prompt context):
1. **API Documentation**: Endpoint specs, request/response models, status codes.
2. **CSV Template**: Target column structure.
3. **Common API Test Cases Checklist**: Master list of required test checks.

> *If any required file is missing, ask the user to attach it before proceeding.*

### Step 2: Apply Generation Skill & Checklist
- Read `common_api_checklist_.md` to load all general/mandatory API test scenarios.
- Apply the rules defined in `api-test-skill.md` for test case logic, coverage, and CSV formatting.

### Step 3: Test Suite Generation
- Cross-reference each API endpoint from the API documentation against the **common_api_checklist**.
- Map mandatory checklist items to specific endpoints (Parameters, Auth, Headers, Error Handling, Boundaries).

### Step 4: Final CSV Formatting
- Format all generated test cases to match the **user_api_checklist** structure.
- Output ONLY the final CSV inside a single markdown code block (` ```csv `) without any commentary.