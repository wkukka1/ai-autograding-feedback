import pytest 
from llm_helpers import *

def test_with_markers(request):
    """ Generates LLM response """
    # Run LLM feedback
    llm_feedback = run_llm(submission="jupyter", question="Question 5b", scope="image", output="stdout",
                           model="claude-3.7-sonnet", prompt="image_style_annotations")
  
    # Display LLM output in the test output
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
    # Add annotations
    add_image_annotations(request, llm_feedback, "student_submission.png")
