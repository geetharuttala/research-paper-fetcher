import subprocess
import sys
import os

def test_cli_help():
    # Force UTF-8 encoding in Windows
    os.environ["PYTHONUTF8"] = "1"
    
    result = subprocess.run(
        ["poetry", "run", "get-papers-list", "-h"],
        capture_output=True,  # Ensure output is captured
        text=True,
        encoding="utf-8",
        errors="replace"  # Replace unsupported characters instead of failing
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    assert result.returncode == 0, f"Error: {result.stderr}"
    assert "Fetch research papers from PubMed" in result.stdout  # Example check

