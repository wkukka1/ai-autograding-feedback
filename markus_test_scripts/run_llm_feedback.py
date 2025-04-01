import subprocess
import pytest
import os
import os.path 


def run_tests():
    result = subprocess.run(
        ["/home/docker/.autotesting/scripts/defaultvenv/bin/python", "-v", "test_bfs.py"], 
        capture_output=True, text=True, check=True
    )
    with open("test_output.txt", "w") as f:
        f.write(result.stdout)
        f.write(result.stderr)
        

def run_llm():
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "python",
        "--prompt", "code_table", # change prompt here
        "--scope", "code",
        "--model", "openai", # change model type here
        "--output", "stdout",
         "--assignment", "./"
    ]

    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip() 
    return llm_output

def test_with_feedback(request):
    """ Generates LLM Feedback """
    # Run tests and capture output as .txt file
    # test_output_file = run_tests()

    # Run LLM feedback
    llm_feedback = run_llm()
    
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
        