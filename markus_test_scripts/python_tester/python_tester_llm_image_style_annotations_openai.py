import pytest
import os
import os.path 
from llm_helpers import *

def test_with_markers(request):
    """ Generates LLM response """
    # Run LLM feedback
    llm_feedback = run_llm(submission="jupyter", question="Question 5b", scope="image", output="stdout",
                           model="openai", prompt="image_style_annotations")
  
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
