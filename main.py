from agents.investigator import investigate
from agents.fixer import generate_fix
from agents.validator import validate_fix

from sandbox.executor import run_in_sandbox
from utils.repo_parser import extract_code


# -------------------------------------------------
# Read repository code
# -------------------------------------------------

with open("demo_repo/calculator.py", "r") as file:
    repository_code = file.read()


# -------------------------------------------------
# Read bug report
# -------------------------------------------------

with open("bug_report.txt", "r") as file:
    bug_report = file.read()


# -------------------------------------------------
# Agent 1: Investigate
# -------------------------------------------------

root_cause = investigate(
    repository_code,
    bug_report
)

print("\n" + "=" * 60)
print("ROOT CAUSE ANALYSIS")
print("=" * 60)

print(root_cause)


# -------------------------------------------------
# Autonomous Fix Loop
# -------------------------------------------------

validator_feedback = ""

MAX_ATTEMPTS = 3

for attempt in range(1, MAX_ATTEMPTS + 1):

    print("\n" + "=" * 60)
    print(f"FIX ATTEMPT {attempt}")
    print("=" * 60)

    # ---------------------------------------------
    # Agent 2: Generate Fix
    # ---------------------------------------------

    fixed_code_response = generate_fix(
        repository_code,
        root_cause,
        validator_feedback
    )

    print(fixed_code_response)

    # ---------------------------------------------
    # Extract pure Python code
    # ---------------------------------------------

    fixed_code = extract_code(
        fixed_code_response
    )

    # ---------------------------------------------
    # Sandbox Testing
    # ---------------------------------------------

    test_result = run_in_sandbox(
        fixed_code,
        "demo_repo"
    )

    test_output = (
        test_result["stdout"]
        + "\n"
        + test_result["stderr"]
    )

    print("\n" + "=" * 60)
    print("SANDBOX TEST RESULTS")
    print("=" * 60)

    print(test_output)

    # ---------------------------------------------
    # If tests pass
    # ---------------------------------------------

    if test_result["success"]:

        print("\nSTATUS: PASSED")

        print("\n" + "=" * 60)
        print("FIX SUCCESSFULLY VALIDATED")
        print("=" * 60)

        break

    # ---------------------------------------------
    # If tests fail
    # ---------------------------------------------

    print("\nSTATUS: FAILED")

    # ---------------------------------------------
    # Agent 3: Validator
    # ---------------------------------------------

    validator_feedback = validate_fix(
        fixed_code,
        test_output,
        root_cause
    )

    print("\n" + "=" * 60)
    print("VALIDATOR AGENT")
    print("=" * 60)

    print(validator_feedback)

else:

    print("\n" + "=" * 60)
    print("FIX COULD NOT BE VALIDATED")
    print("=" * 60)