import os, sys
from helpers.arg_options import model_mapping
from helpers.file_converter import rename_files
from pathlib import Path

EXPECTED_SUFFIXES = ["_solution", "test_output", "_submission"]


def process_code(args, prompt):
    prompt = prompt["prompt_content"]
    
    # Determine the assignment folder
    
    # assignment_folder = f"{TEST_ASSIGNMENT_DIRECTORY}/{args.assignment}"
    assignment_folder = "./"
    if not os.path.exists(assignment_folder):
        raise FileNotFoundError(f"Assignment folder '{assignment_folder}' not found.")

    if args.submission_type == "jupyter":
        ensure_txt_files(assignment_folder, rename_files)

        # Load only the required .txt files into assignment_files
        assignment_files = [
            os.path.join(assignment_folder, f)
            for f in os.listdir(assignment_folder)
            if os.path.isfile(os.path.join(assignment_folder, f)) and any(f.endswith(suffix + ".txt") for suffix in EXPECTED_SUFFIXES)
        ]
    elif args.submission_type == "python":
        # Load only the required .txt files into assignment_files
        assignment_files = [
            os.path.join(assignment_folder, f)
            for f in os.listdir(assignment_folder)
            if os.path.isfile(os.path.join(assignment_folder, f)) and any(os.path.splitext(f)[0].endswith(suffix) for suffix in EXPECTED_SUFFIXES)
        ]
    
    # Create model 
    if args.model in model_mapping:
        model = model_mapping[args.model]()
    else:
        print("Invalid model selected for code scope.")
        sys.exit(1)
    
    if args.scope == "code":
        if args.question:
            request, response = model.generate_response(prompt, assignment_files, question_num=args.question)
        else:
            request, response = model.generate_response(prompt, assignment_files)
                      
    return request, response


def ensure_txt_files(directory, rename_function):
    """Ensure required .txt files exist. Convert only missing ones."""
    missing_suffixes = []
    
    for suffix in EXPECTED_SUFFIXES:
        if not any(f.endswith(suffix + ".txt") for f in os.listdir(directory)):
            missing_suffixes.append(suffix)

    if missing_suffixes:
        for filename in os.listdir(directory):
            file_path = Path(directory) / filename  # Create a Path object
            file_base, ext = file_path.stem, file_path.suffix 

            for suffix in missing_suffixes:
                if file_base.endswith(suffix) and ext != ".txt":
                    if file_path.is_file():
                        rename_function(file_path)
                    break