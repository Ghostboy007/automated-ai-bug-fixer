from utils.llm import ask_llm


def investigate(repository_code, bug_report):

    prompt = f"""
You are a senior software debugging engineer.

Analyze the following source code and bug report.

SOURCE CODE:
{repository_code}

BUG REPORT:
{bug_report}

Your task is to identify:

1. Affected file
2. Affected function
3. Root cause
4. Evidence from the code
5. Recommended fix

Do NOT modify the code.

Return a concise but clear Root Cause Analysis.
"""

    return ask_llm(prompt)