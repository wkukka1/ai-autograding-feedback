import json
import subprocess
import pytest
import os
import os.path 
import re

        
def run_llm() -> str:
    """Run the LLM feedback generator and return results"""
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "jupyter",
        "--prompt", "image_analyze_annotations",
        "--scope", "image",
        "--assignment", "./",
        "--question", "Question 5b",
        "--model", "openai",
        "--output", "stdout"
    ]

    # Capture the output from the LLM program
    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()
    return llm_output

def extract_json(response) -> list[dict]:
    match = re.search(r"\`\`\`json([\S\s]+)\`\`\`", response)
    if match:
        return json.loads(match.group(1))
    return []

DEFAULT_ANNOTATION_WIDTH = 25
def convert_coordinates(coordinate_pair: list[int]) -> tuple[int]:
    return (
        coordinate_pair[0],
        coordinate_pair[1],
        coordinate_pair[0] + DEFAULT_ANNOTATION_WIDTH,
        coordinate_pair[1] + DEFAULT_ANNOTATION_WIDTH
    )

def test_with_markers(request):
    """ Generates LLM response """
    # Run LLM feedback
    llm_feedback = run_llm()
  
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))

    outputs = extract_json(llm_feedback)

    for output in outputs:
        x1, y1, x2, y2 = convert_coordinates(output["location"])
        request.node.add_marker(pytest.mark.markus_annotation(
            type="ImageAnnotation",
            filename=os.path.relpath("student_submission.png", os.getcwd()),
            content=output["description"],
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        ))
