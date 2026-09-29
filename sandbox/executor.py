import os
import shutil
import subprocess
import tempfile


def run_in_sandbox(original_code, test_directory):
    """
    Creates a temporary sandbox, copies the test files,
    replaces the source code with the AI-generated version,
    and runs pytest.
    """

    sandbox_dir = tempfile.mkdtemp(prefix="bugfix_sandbox_")

    try:
        # Copy the existing test file
        # Copy all test files into sandbox

     for filename in os.listdir(test_directory):

      if filename.startswith("test_") and filename.endswith(".py"):

        source_test = os.path.join(
            test_directory,
            filename
        )

        sandbox_test = os.path.join(
            sandbox_dir,
            filename
        )

        shutil.copy(source_test, sandbox_test)

        # Write AI-generated source code
        source_file = os.path.join(
            sandbox_dir,
            "calculator.py"
        )

        with open(source_file, "w") as file:
            file.write(original_code)

        # Run pytest inside sandbox
        result = subprocess.run(
            ["pytest", "-q"],
            cwd=sandbox_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "sandbox_path": sandbox_dir
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Test execution timed out.",
            "sandbox_path": sandbox_dir
        }

    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "sandbox_path": sandbox_dir
        }