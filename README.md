# 🐛 Autonomous AI Bug Fixer

An autonomous multi-agent AI system that investigates software bugs, generates code fixes, tests them in an isolated sandbox, and uses validation feedback to iteratively improve the fix.

---

## 📌 Project Overview

Software debugging usually requires developers to manually:

1. Understand the bug report
2. Find the root cause
3. Modify the source code
4. Run tests
5. Analyze failures
6. Modify the code again if required

The Autonomous AI Bug Fixer automates this workflow using multiple AI agents.

The system takes a source code file and a bug report as input and creates an autonomous feedback loop:

**Investigate → Fix → Test → Validate → Retry**

The project uses a local Llama 3.2 model through Ollama, so the AI processing can run locally.

---

## 🏗️ System Architecture

The system consists of four major components:

### 1. Investigator Agent

Analyzes the source code and bug report.

It identifies:

- Affected file
- Affected function
- Root cause
- Evidence from the code
- Recommended fix

It does not modify the source code.

### 2. Fix Generator Agent

Uses the root-cause analysis to generate a corrected version of the source code.

It also receives feedback from the Validator Agent when a previous fix fails.

The agent is instructed to:

- Fix the identified bug
- Preserve existing functionality
- Avoid unrelated changes
- Return the complete corrected source code

### 3. Sandbox Executor

The generated code is not directly executed on the main project.

Instead, the system:

1. Creates a temporary directory
2. Copies the test files into the directory
3. Places the AI-generated source code there
4. Runs the test suite using Pytest
5. Captures the test output

This provides an isolated environment for testing the generated fix.

### 4. Validator Agent

The Validator Agent analyzes the sandbox test results.

It determines:

- Whether the bug was fixed
- Whether regression occurred
- Why a test failed
- What feedback should be given to the Fix Generator

If the fix fails, the feedback is sent back to the Fix Generator and another attempt is made.

---

## 🔄 Autonomous Workflow

```text
                 Bug Report
                     │
                     ▼
            ┌─────────────────┐
            │ Investigator    │
            │ Agent           │
            └────────┬────────┘
                     │
               Root Cause
                     │
                     ▼
            ┌─────────────────┐
            │ Fix Generator   │
            │ Agent           │
            └────────┬────────┘
                     │
                Generated Fix
                     │
                     ▼
            ┌─────────────────┐
            │ Sandbox         │
            │ Executor        │
            └────────┬────────┘
                     │
                  Pytest
                     │
                     ▼
            ┌─────────────────┐
            │ Validator       │
            │ Agent           │
            └────────┬────────┘
                     │
              ┌──────┴──────┐
              │             │
            PASS           FAIL
              │             │
              ▼             ▼
          Final Fix     Feedback
                            │
                            └──────► Fix Generator