TEST_OUTPUTS_DIRECTORY = "test_responses_md"
HELP_MESSAGES = {
    "submission_type": "The format of the submission file (e.g., Jupyter notebook, Python script).",
    "prompt": "Pre-defined prompt name (from ai_feedback/data/prompts/user/) or file path to custom prompt file.",
    "prompt_text": "Additional messages to concatenate to the prompt.",
    "scope": "The section of the assignment the model should analyze (e.g., code or image).",
    "submission": "The file path for the submission file.",
    "solution": "The file path for the solution file.",
    "question": "The specific question number to analyze within the assignment (if applicable).",
    "model": "The name of the LLM model to use for evaluation.",
    "remote_model": "When using --remote=model, this option specifies the remote model to use.",
    "output": "Format to display the output response.",
    "llama_mode": "Specifies how to invoke llama.cpp: either directly via its command‐line interface (CLI) or by sending requests to a running llama-server instance.",
    "test_output": "The output of tests from evaluating the assignment.",
    "submission_image": "The file path for the image file.",
    "solution_image": "The file path to the solution image.",
    "system_prompt": "Pre-defined system prompt name (from ai_feedback/data/prompts/system/) or file path to custom system prompt file.",
}
