import os
import sys
from pathlib import Path
from typing import Callable, List, Tuple

from .helpers.arg_options import model_mapping
from .helpers.file_converter import rename_files
from .helpers.template_utils import render_prompt_template

EXPECTED_SUFFIXES = ["_solution", "test_output", "_submission"]


def process_code(args, prompt: str) -> Tuple[str, str]:
    """
    Processes assignment files and generates a response using the selected model.

    Depending on the submission type (Jupyter or Python), it loads the appropriate
    files from the assignment folder, modifies the prompt with file references,
    and invokes the selected model to generate a response.

    Args:
        args: Command-line argument namespace containing submission_type, assignment, model, scope, and question.
        prompt (str): The initial user prompt to be modified and passed to the model.

    Returns:
        Tuple[str, str]: A tuple containing the final request string and the model's generated response.

    Raises:
        FileNotFoundError: If the assignment folder does not exist.
        SystemExit: If an invalid model is selected.
    """
    assignment_folder = f"{args.assignment}"
    if not os.path.exists(assignment_folder):
        raise FileNotFoundError(f"Assignment folder '{assignment_folder}' not found.")

    assignment_files: List[str] = []

    if args.submission_type == "jupyter":
        ensure_txt_files(
            assignment_folder, rename_files
        )  # Convert notebooks to .txt if needed

        assignment_files = [
            os.path.join(assignment_folder, f)
            for f in os.listdir(assignment_folder)
            if os.path.isfile(os.path.join(assignment_folder, f))
            and any(f.endswith(suffix + ".txt") for suffix in EXPECTED_SUFFIXES)
        ]

    elif args.submission_type == "python":
        assignment_files = [
            os.path.join(assignment_folder, f)
            for f in os.listdir(assignment_folder)
            if os.path.isfile(os.path.join(assignment_folder, f))
            and any(
                os.path.splitext(f)[0].endswith(suffix) for suffix in EXPECTED_SUFFIXES
            )
        ]

    prompt = render_prompt_template(prompt, assignment_files=assignment_files)

    if args.model in model_mapping:
        model = model_mapping[args.model]()
    else:
        print("Invalid model selected for code scope.")
        sys.exit(1)

    if args.scope == "code":
        if args.question:
            request, response = model.generate_response(
                prompt=prompt,
                assignment_files=assignment_files,
                question_num=args.question,
            )
        else:
            request, response = model.generate_response(
                prompt=prompt, assignment_files=assignment_files
            )

    return request, response


def ensure_txt_files(directory: str, rename_function: Callable[[Path], None]) -> None:
    """
    Ensures that required .txt files exist in the directory.
    Converts missing files through a helper function found in helpers/file_converter.

    Args:
        directory (str): Path to the assignment directory.
        rename_function (Callable[[Path], None]): A function that handles renaming or converting files.

    Returns:
        None
    """
    missing_suffixes: List[str] = []

    for suffix in EXPECTED_SUFFIXES:
        if not any(f.endswith(suffix + ".txt") for f in os.listdir(directory)):
            missing_suffixes.append(suffix)

    if missing_suffixes:
        for filename in os.listdir(directory):
            file_path = Path(directory) / filename
            file_base, ext = file_path.stem, file_path.suffix

            for suffix in missing_suffixes:
                if file_base.endswith(suffix) and ext != ".txt":
                    if file_path.is_file():
                        rename_function(file_path)
                    break
