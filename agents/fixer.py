from utils.llm import ask_llm


def generate_fix(
    repository_code,
    root_cause,
    validator_feedback=""
):

    prompt = f"""
You are an expert software engineer responsible
for fixing bugs.

SOURCE CODE:
{repository_code}

ROOT CAUSE ANALYSIS:
{root_cause}

VALIDATOR FEEDBACK:
{validator_feedback}

Your task is to generate a corrected version
of the source code.

Rules:

1. Fix the identified bug.
2. Carefully follow the validator feedback.
3. Do not change unrelated functionality.
4. Preserve existing function names and interfaces.
5. Return the COMPLETE corrected source code.
6. Do not simply explain the fix.
7. Make sure the generated code satisfies the
   failing test.

Use this exact format:

---BEGIN CODE---
<complete corrected source code>
---END CODE---

---BEGIN EXPLANATION---
<short explanation>
---END EXPLANATION---
"""

    return ask_llm(prompt)