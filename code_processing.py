import os, sys
from models.CodeLlamaModel import CodeLlamaModel
from models.OpenAIModel import OpenAIModel
from models.DeepSeekModel import DeepSeekModel
from helpers.constants import TEST_ASSIGNMENT_DIRECTORY

def process_code(args, prompt):
    prompt = prompt["prompt_content"]
    
    # Determine the assignment folder
    assignment_folder = f"{TEST_ASSIGNMENT_DIRECTORY}/{args.assignment}"
    if not os.path.exists(assignment_folder):
        raise FileNotFoundError(f"Assignment folder '{assignment_folder}' not found.")

    # Load all files in the assignment folder to provide them to the API call
    assignment_files = [os.path.join(assignment_folder, f) for f in os.listdir(assignment_folder) if os.path.isfile(os.path.join(assignment_folder, f))]

    # Create model 
    if args.model == "deepSeek-R1:70B":
        model = DeepSeekModel()
    elif args.model == "openai":
        model = OpenAIModel()
    elif args.model == "codellama:latest": 
        model = CodeLlamaModel()
    else: 
        print("Invalid model selected for code scope.")
        sys.exit(1)
    
    if args.scope == "code":
        if args.question:
            request, response = model.generate_response(prompt, assignment_files, question_num=args.question)
        else:
            request, response = model.generate_response(prompt, assignment_files)
                      
    return request, response