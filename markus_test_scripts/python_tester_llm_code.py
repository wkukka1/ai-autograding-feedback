import subprocess
import pytest
import os
import os.path 
import json 
from llm_helpers import extract_json, ANNOTATION_PROMPT, add_annotation_columns

# Modify depending on name of student's submission file 
import cnn_submission as submission

# NOTE: add numpy and torch in package requirements section of autotester settings 

llm_feedback = ''

def run_llm():
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "python",
        "--prompt", "code_table", # change prompt type here 
        "--scope", "code",
        "--model", "claude-3.7-sonnet", # change model type here
        "--output", "stdout",
        "--assignment", "./"
    ]

    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()
    return llm_output

def test_with_feedback(request):
    """ Generates LLM Feedback """
    global llm_feedback 
    llm_feedback = run_llm() # get LLM feedback and display on markus
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
        
 
def run_llm_annotation():
    # feed in previous LLM message to create annotations
    prompt = f"Previous message: {llm_feedback}."
    prompt += ANNOTATION_PROMPT
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "python",
        "--prompt_text", prompt, 
        "--scope", "code",
        "--model", "claude-3.7-sonnet", # change model type here
        "--output", "direct",
        "--assignment", "./"
    ]

    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()
    return llm_output

def test_with_annotations(request):
    """ Generates LLM Annotations """

    # Run LLM feedback
    raw_annotation = run_llm_annotation() # generate annotations
    annotations = extract_json(raw_annotation) 
    annotations = json.loads(annotations)["annotations"]
    
    annotations_with_columns = add_annotation_columns(annotations, submission)
    
    request.node.add_marker(pytest.mark.markus_message(str(annotations_with_columns)))
    
    for annotation in annotations_with_columns:
        filename = annotation["filename"]
        content = annotation["content"]
        line_start = annotation["line_start"]
        line_end = annotation["line_end"]
        column_start = annotation["column_start"]
        column_end = annotation["column_end"]

        # Convert filename to relative path
        rel_filename = os.path.relpath(filename, os.getcwd())

        # Add pytest marker for each annotation separately
        request.node.add_marker(pytest.mark.markus_annotation(
            filename=rel_filename,
            content=content,
            line_start=line_start,
            line_end=line_end,
            column_start=column_start,
            column_end=column_end,
        ))

