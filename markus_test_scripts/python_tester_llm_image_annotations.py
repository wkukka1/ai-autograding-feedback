import subprocess
import pytest
import os
import os.path 
import re

        
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
        "--output", "direct"
    ]

    # Capture the output from the LLM program
    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()  # Process output if needed
    return llm_output

DEFAULT_ANNOTATION_WIDTH = 25
def extract_coordinates(response):
    """Returns all coordinates found in response as a list of boxes (x1, y1, x2, y2)"""
    matches: list[tuple[str]] = re.findall(r"[([](\d+(?:-\d+)?),\s*(\d+(?:-\d+)?)[])]", response)
    coordinate_boxes: list[tuple[int]] = []
    for match in matches:
        if "-" in match[0]:
            x1, x2 = int(match[0].split("-")[0]), int(match[0].split("-")[1])
        else:
            x1 = int(match[0])
            x2 = x1 + DEFAULT_ANNOTATION_WIDTH

        if "-" in match[1]:
            y1, y2 = int(match[1].split("-")[0]), int(match[1].split("-")[1])
        else:
            y1 = int(match[1])
            y2 = y1 + DEFAULT_ANNOTATION_WIDTH
        coordinate_boxes.append((x1, y1, x2, y2))
    return coordinate_boxes

def test_with_markers(request):
    """ Generates LLM response """
    # Run LLM feedback
    llm_feedback = run_llm()
  
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))

    coordinate_boxes = extract_coordinates(llm_feedback)[0]
    x1, y1, x2, y2 = coordinate_boxes
    request.node.add_marker(pytest.mark.markus_annotation(
        filename=os.path.relpath("student_submission.png", os.getcwd()),
        content=llm_feedback,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
    ))

print(extract_coordinates("askljdh a(2, 100)asd as[321,99-121]hdth(20-50, 40)fg"))