SYSTEM_INSTRUCTIONS = """You are a helpful assistant that provides detailed feedback on students' test errors.
Your goal is to identify mistakes in their assignments, explain why the mistakes occurred,
and offer guidance on how to correct them. Ensure the feedback is clear, supportive, and
encourages improvement."""
TEST_OUTPUTS_DIRECTORY = "test_responses_md"
HELP_MESSAGES = {
    "submission_type": "The format of the submission file (e.g., Jupyter notebook, Python script).",
    "prompt": "The specific prompt to use for evaluating the assignment.",
    "prompt_text": "Additional messages to concatenate to the prompt.",
    "scope": "The section of the assignment the model should analyze (e.g., code or image).",
    "assignment": "The name of the assignment to be evaluated.",
    "question": "The specific question number to analyze within the assignment (if applicable).",
    "model": "The name of the LLM model to use for evaluation.",
    "output": "Format to display the output response."
}