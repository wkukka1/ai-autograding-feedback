import pytest
from llm_helpers import *


def test_with_markers(request):
    """Generates LLM response for PDF submission"""
    # Run LLM feedback
    llm_feedback = run_llm(
        submission_path="student_submission.pdf",
        scope="text",
        model="openai",
        prompt="text_pdf_analyze",
    )

    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
