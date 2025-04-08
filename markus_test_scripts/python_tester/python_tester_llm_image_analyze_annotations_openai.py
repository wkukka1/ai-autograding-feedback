import pytest
from llm_helpers import *

def test_image_analyze(request):
    """Test whether the submission graph matches the problem requirements"""
    # Run LLM feedback
    llm_feedback = run_llm(submission="jupyter", question="Question 5b", scope="image", output="stdout",
                           model="openai", prompt="image_analyze_annotations")
  
    # Display LLM output in the test output
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
    # Add annotations
    add_image_annotations(request, llm_feedback, "student_submission.png")
