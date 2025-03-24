import subprocess
import pytest
import os
import os.path 

def run_tests():
    result = subprocess.run(
        ["/home/docker/.autotesting/scripts/defaultvenv/bin/python", "-v", "test_bfs.py"],  # Replace with your test file
        capture_output=True, text=True, check=True  # `check=True` raises error if pytest fails
    )
    with open("test_output.txt", "w") as f:
        f.write(result.stdout)  # Write test output to the file
        f.write(result.stderr)  # Optionally capture errors too
        
#claude-3.7-sonnet
def run_llm():
    # Pass test_output as part of the input to the LLM program
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "python",
        "--prompt", "code_lines",
        "--scope", "code",
        "--model", "claude-3.7-sonnet",
        "--output", "stdout"
    ]

    # Capture the output from the LLM program
    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()  # Process output if needed
    return llm_output

def test_with_markers(request):
    """ Generates LLM response """
    # Run tests and capture output as .txt file
    test_output_file = run_tests()

    # Run LLM feedback
    llm_feedback = run_llm()
  
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))