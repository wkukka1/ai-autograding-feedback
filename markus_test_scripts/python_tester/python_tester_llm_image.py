import subprocess
import pytest
import os
import os.path 

        
def run_llm():
    # Pass test_output as part of the input to the LLM program
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "jupyter",
        "--prompt", "image_style",
        "--scope", "image",
        "--assignment", "./",
        "--question", "Question 5b",
        "--model", "openai",
        "--output", "stdout"
    ]

    # Capture the output from the LLM program
    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()  # Process output if needed
    return llm_output


def test_with_markers(request):
    """ Generates LLM response """
    # Run LLM feedback
    llm_feedback = run_llm()
  
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
