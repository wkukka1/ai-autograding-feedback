import os, sys
from helpers.constants import TEST_ASSIGNMENT_DIRECTORY
from helpers.arg_options import model_mapping

def process_code(args, prompt):
    prompt = prompt["prompt_content"]
    
    # Determine the assignment folder
    assignment_folder = f"{TEST_ASSIGNMENT_DIRECTORY}/{args.assignment}"
    if not os.path.exists(assignment_folder):
        raise FileNotFoundError(f"Assignment folder '{assignment_folder}' not found.")

    # Load all files in the assignment folder to provide them to the API call
    assignment_files = [os.path.join(assignment_folder, f) for f in os.listdir(assignment_folder) if os.path.isfile(os.path.join(assignment_folder, f))]

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