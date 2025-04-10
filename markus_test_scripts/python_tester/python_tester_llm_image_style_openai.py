import pytest
from llm_helpers import *

def test_with_markers(request):
    """ Generates LLM response """
    # Run LLM feedback
    llm_feedback = run_llm(submission="jupyter", question="Question 5b", scope="image", output="stdout",
                           model="openai", prompt="image_style")
  
    # Display LLM output in the test output
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
