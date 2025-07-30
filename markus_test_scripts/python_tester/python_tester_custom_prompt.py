import pytest
from llm_helpers import *

llm_feedback = ""


def test_with_feedback(request):
    """Generates LLM Feedback using instructor's custom prompt file."""
    global llm_feedback

    # change prompt and model here
    # instructor uploaded custom_prompt.txt file
    llm_feedback = run_llm(
        prompt_text="custom_prompt",
        submission_path='student_submission.py',
        scope="code",
        model="claude-3.7-sonnet",
    )
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
