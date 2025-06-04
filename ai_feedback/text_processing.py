import os
import sys
from pathlib import Path
from typing import Tuple, List

from .helpers.arg_options import model_mapping
from .helpers.template_utils import render_prompt_template

EXPECTED_SUFFIXES = ["_solution", "_submission"]


def process_text(args, prompt: str) -> Tuple[str, str]:
    """
    Processes text-based assignment files and generates a response using the selected model.

    This function looks for files matching specific suffixes in the provided assignment folder,
    updates the user prompt to reference these files, and invokes a model to generate feedback
    or analysis based on the provided scope and question.

    Args:
        args: Command-line argument namespace containing assignment, model, scope, and question attributes.
        prompt (str): The initial user prompt.

    Returns:
        Tuple[str, str]: A tuple containing the request and the model's generated response.

    Raises:
        FileNotFoundError: If the specified assignment folder does not exist.
        SystemExit: If the model name provided in args is not recognized.
    """
    assignment_folder = f"{args.assignment}"
    if not os.path.exists(assignment_folder):
        raise FileNotFoundError(f"Assignment folder '{assignment_folder}' not found.")

    assignment_files: List[str] = [
        os.path.join(assignment_folder, f)
        for f in os.listdir(assignment_folder)
        if os.path.isfile(os.path.join(assignment_folder, f))
        and any(os.path.splitext(f)[0].endswith(suffix) for suffix in EXPECTED_SUFFIXES)
    ]

    rendered_prompt = render_prompt_template(prompt, assignment_files=assignment_files)

    if args.model in model_mapping:
        model = model_mapping[args.model]()
    else:
        print("Invalid model selected for text scope.")
        sys.exit(1)

    if args.question:
        request, response = model.generate_response(
            prompt=rendered_prompt,
            assignment_files=assignment_files,
            question_num=args.question,
        )
    else:
        request, response = model.generate_response(
            prompt=rendered_prompt, assignment_files=assignment_files
        )

    return request, response
