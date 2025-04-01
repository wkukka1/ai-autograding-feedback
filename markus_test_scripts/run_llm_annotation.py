import subprocess
import pytest
import os
import os.path 
import json 

import re

def run_tests():
    result = subprocess.run(
        ["/home/docker/.autotesting/scripts/defaultvenv/bin/python", "-v", "test_bfs.py"],  # Replace with your test file
        capture_output=True, text=True, check=True 
    )
    with open("test_output.txt", "w") as f:
        f.write(result.stdout) 
        f.write(result.stderr) 
        

def run_llm_annotation():
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "python",
        "--prompt", "code_annotation", # run annotation prompt
        "--scope", "code",
        "--model", "openai",
        "--output", "direct",
        "--assignment", "./"
    ]

    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip() 
    return llm_output

def test_with_annotations(request):
    """ Generates LLM Annotations """
    # Run tests and capture output as .txt file
    #test_output_file = run_tests()

    # Run LLM feedback
    raw_annotation = run_llm_annotation()
    request.node.add_marker(pytest.mark.markus_message(raw_annotation))
    
    annotation = extract_json(raw_annotation)
    
    annotations = json.loads(annotation)["annotations"]
    
    for annotation in annotations:
        filename = annotation["filename"]
        content = annotation["content"]
        line_start = annotation["line_start"]
        line_end = annotation["line_end"]
        column_start = annotation["column_start"]
        column_end = annotation["column_end"]

        # Convert filename to relative path
        rel_filename = os.path.relpath(filename, os.getcwd())

        # Add pytest marker
        request.node.add_marker(pytest.mark.markus_annotation(
            filename=rel_filename,
            content=content,
            line_start=line_start,
            line_end=line_end,
            column_start=column_start,
            column_end=column_end,
        ))

def extract_json(text):
    """Extracts the JSON object containing 'annotations' from the model's output."""
    match = re.search(r'(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})', text)
    if not match:
        return "No valid JSON found in the response."
    
    json_str = match.group(1)  # Extract the matched JSON string
    
    try:
        return json_str
    except json.JSONDecodeError as e:
        return "Error parsing JSON."