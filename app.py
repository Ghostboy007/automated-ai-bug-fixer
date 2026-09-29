import streamlit as st
import os
import difflib

from agents.investigator import investigate
from agents.fixer import generate_fix
from agents.validator import validate_fix

from sandbox.executor import run_in_sandbox
from utils.repo_parser import extract_code


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Autonomous AI Bug Fixer",
    page_icon="🐛",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.stage {
    padding: 15px;
    border-radius: 10px;
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.success-box {
    padding: 18px;
    border-radius: 10px;
    background-color: #e8f7ee;
    border: 1px solid #a7dfbd;
}

.failure-box {
    padding: 18px;
    border-radius: 10px;
    background-color: #fff0f0;
    border: 1px solid #ffb3b3;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">🐛 Autonomous AI Bug Fixer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Multi-agent AI system that investigates, fixes, tests and validates software bugs autonomously.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Configuration")

    max_attempts = st.slider(
        "Maximum Fix Attempts",
        min_value=1,
        max_value=5,
        value=3
    )

    st.markdown("---")

    st.markdown("### 🤖 AI Pipeline")

    st.write("🔍 Investigator Agent")
    st.write("🛠️ Fix Generator Agent")
    st.write("🧪 Sandbox Executor")
    st.write("✅ Validator Agent")
    st.write("🔄 Autonomous Retry Loop")


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("📂 Source Code")

    default_code = """def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b
"""

    source_code = st.text_area(
        "Enter the buggy source code",
        value=default_code,
        height=300
    )


with col2:

    st.subheader("🐛 Bug Report")

    default_bug = """The calculator application crashes when a user
attempts to divide a number by zero.

Error:
ZeroDivisionError: division by zero

Expected behavior:
The application should handle division by zero gracefully
instead of crashing.
"""

    bug_report = st.text_area(
        "Describe the bug",
        value=default_bug,
        height=300
    )


# --------------------------------------------------
# RUN BUTTON
# --------------------------------------------------

run_button = st.button(
    "🚀 Run Autonomous Bug Fixer",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

if run_button:

    # ----------------------------------------------
    # INVESTIGATOR
    # ----------------------------------------------

    with st.status(
        "🔍 Investigator Agent analyzing the bug...",
        expanded=True
    ):

        root_cause = investigate(
            source_code,
            bug_report
        )

        st.markdown("### Root Cause Analysis")

        st.write(root_cause)


    # ----------------------------------------------
    # AUTONOMOUS LOOP
    # ----------------------------------------------

    validator_feedback = ""

    successful_code = None
    successful_attempt = None

    attempts_data = []


    for attempt in range(1, max_attempts + 1):

        st.markdown("---")

        st.subheader(
            f"🔄 Fix Attempt {attempt}"
        )


        # ------------------------------------------
        # FIX GENERATOR
        # ------------------------------------------

        with st.spinner(
            f"Fix Generator is generating fix #{attempt}..."
        ):

            fixed_response = generate_fix(
                source_code,
                root_cause,
                validator_feedback
            )

            fixed_code = extract_code(
                fixed_response
            )


        with st.expander(
            f"🛠️ Generated Fix — Attempt {attempt}"
        ):

            st.code(
                fixed_code,
                language="python"
            )


        # ------------------------------------------
        # SANDBOX
        # ------------------------------------------

        with st.spinner(
            "🧪 Running tests in isolated sandbox..."
        ):

            test_result = run_in_sandbox(
                fixed_code,
                "demo_repo"
            )


        test_output = (
            test_result["stdout"]
            + "\n"
            + test_result["stderr"]
        )


        with st.expander(
            f"🧪 Sandbox Test Results — Attempt {attempt}"
        ):

            st.code(
                test_output,
                language="text"
            )


        attempts_data.append({
            "attempt": attempt,
            "code": fixed_code,
            "test_output": test_output,
            "success": test_result["success"]
        })


        # ------------------------------------------
        # SUCCESS
        # ------------------------------------------

        if test_result["success"]:

            successful_code = fixed_code
            successful_attempt = attempt

            st.markdown(
                '<div class="success-box">'
                '<h3>✅ Fix Successfully Validated</h3>'
                f'<p>Validated after {attempt} attempt(s).</p>'
                '</div>',
                unsafe_allow_html=True
            )

            break


        # ------------------------------------------
        # VALIDATOR
        # ------------------------------------------

        with st.spinner(
            "🤖 Validator Agent analyzing failure..."
        ):

            validator_feedback = validate_fix(
                fixed_code,
                test_output,
                root_cause
            )


        with st.expander(
            f"🤖 Validator Feedback — Attempt {attempt}"
        ):

            st.write(
                validator_feedback
            )


    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    st.markdown("---")

    st.header("📊 Final Result")


    if successful_code:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Status",
                "PASS"
            )

        with col2:
            st.metric(
                "Attempts",
                successful_attempt
            )

        with col3:
            st.metric(
                "Validation",
                "Successful"
            )


        # ------------------------------------------
        # PATCH
        # ------------------------------------------

        st.subheader("📌 Generated Patch")

        diff = difflib.unified_diff(
            source_code.splitlines(),
            successful_code.splitlines(),
            fromfile="calculator.py (original)",
            tofile="calculator.py (fixed)",
            lineterm=""
        )

        diff_text = "\n".join(diff)

        st.code(
            diff_text,
            language="diff"
        )


        # ------------------------------------------
        # PR SUMMARY
        # ------------------------------------------

        st.subheader("📋 Pull Request Summary")

        st.markdown(f"""
**Bug:** Division by zero causes application failure.

**Root Cause:**  
The `divide()` function does not handle a zero denominator.

**Fix:**  
The generated implementation explicitly handles division by zero.

**Validation:**  
The fix was executed in a temporary sandbox and validated using automated tests.

**Autonomous Attempts:**  
{successful_attempt}

**Final Status:**  
✅ Ready for human review
""")


        # ------------------------------------------
        # FIXED CODE
        # ------------------------------------------

        st.subheader("💻 Validated Source Code")

        st.code(
            successful_code,
            language="python"
        )


    else:

        st.markdown(
            '<div class="failure-box">'
            '<h3>❌ Fix Could Not Be Validated</h3>'
            '<p>The autonomous loop reached the maximum number of attempts.</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            "Review the validator feedback and increase the maximum "
            "number of attempts if necessary."
        )