from utils.llm import ask_llm


def validate_fix(
    fixed_code,
    test_output,
    root_cause
):

    prompt = f"""
You are a senior software validation engineer.

A software bug was identified and an AI-generated fix
was tested in a sandbox.

ROOT CAUSE:
{root_cause}

GENERATED CODE:
{fixed_code}

TEST RESULTS:
{test_output}

Analyze the test results.

Determine:

1. Did the fix successfully solve the reported bug?
2. Did any regression occur?
3. What caused any failed tests?
4. If the fix failed, provide precise feedback
   for the Fix Generator.

Return:

STATUS: PASS or FAIL

ANALYSIS:
<your analysis>

FIX FEEDBACK:
<feedback for the Fix Generator>
"""

    return ask_llm(prompt)