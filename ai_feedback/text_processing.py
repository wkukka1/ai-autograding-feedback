import os
import sys
from pathlib import Path
from typing import Tuple, List

from .helpers.arg_options import model_mapping


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
    submission_file = Path(args.submission)
    if not submission_file.is_file():
        raise FileNotFoundError(f"Submission file '{submission_file}' not found.")
    solution_file = None
    if args.solution and args.solution != '':
        solution_file = Path(args.solution)
        if not solution_file.is_file():
            raise FileNotFoundError(f"Solution file '{solution_file}' not found.")

    prompt += (
        f"\nThe student's code submission file you should reference is "
        f"{submission_file}."
    )
    if solution_file:
        prompt += (
            f"\nThe instructor's solution file you should reference is "
            f"{solution_file}."
        )

    if args.model in model_mapping:
        model = model_mapping[args.model]()
    else:
        print("Invalid model selected for text scope.")
        sys.exit(1)

    if args.scope == "text":
        if args.question:
            request, response = model.generate_response(
                prompt=prompt,
                solution_file=solution_file,
                submission_file=submission_file,
                question_num=args.question,
            )
        else:
            request, response = model.generate_response(
                prompt=prompt,
                solution_file=solution_file,
                submission_file=submission_file,
            )

    return request, response
