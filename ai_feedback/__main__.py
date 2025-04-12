import argparse
import json
import os
import os.path
import sys
from datetime import datetime
from . import image_processing
from . import code_processing
from . import text_processing
from .helpers import arg_options
from .helpers.constants import TEST_OUTPUTS_DIRECTORY, HELP_MESSAGES

def load_markdown_template():
    # Load the Markdown template from an external file
    try:
        template_file = os.path.join(os.path.dirname(__file__), 'data/output/output_template.md')
        with open(template_file, "r") as template_file:
            return template_file.read()
    except FileNotFoundError:
        print("Error: Markdown template file 'output_template.md' not found.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--submission_type", type=str, choices=arg_options.get_enum_values(arg_options.FileType), required=True, help=HELP_MESSAGES["submission_type"])
    parser.add_argument("--prompt", type=str, choices=arg_options.get_enum_values(arg_options.Prompt), required=False, help=HELP_MESSAGES["prompt"])
    parser.add_argument("--prompt_text", type=str, required=False, help=HELP_MESSAGES["prompt_text"])
    parser.add_argument("--prompt_custom", action="store_true", required=False)
    parser.add_argument("--scope", type=str, choices=arg_options.get_enum_values(arg_options.Scope), required=True, help=HELP_MESSAGES["scope"])
    parser.add_argument("--assignment", type=str, required=True, help=HELP_MESSAGES["assignment"])
    parser.add_argument("--question", type=str, required=False, help=HELP_MESSAGES["question"])
    parser.add_argument("--model", type=str, choices=arg_options.get_enum_values(arg_options.Models), required=True, help=HELP_MESSAGES["model"])
    parser.add_argument("--output", type=str, choices=arg_options.get_enum_values(arg_options.OutputType), required=True, help=HELP_MESSAGES["output"])

    args = parser.parse_args()

    # Open prompt file
    if args.prompt_custom: 
        prompt_filename = os.path.join(os.path.dirname(__file__), f'./home/docker/.autotesting/scripts/{args.prompt_text}.txt')
        with open(prompt_filename, "r") as prompt_file:
            prompt_content += prompt_file.read()
    else: 
        prompt_content = ''
        if args.prompt:
            # Ensure scope and prompt selected align
            if not args.prompt.startswith("image") and args.scope == "image":
                print("Error: The prompt must start with 'image'. Please re-run the command with a valid prompt.")
                sys.exit(1)
            if not args.prompt.startswith("code") and args.scope == "code":
                print("Error: The prompt must start with 'image'. Please re-run the command with a valid prompt.")
                sys.exit(1)
            if not args.prompt.startswith("text") and args.scope == "text":
                print("Error: The prompt must start with 'text'. Please re-run the command with a valid prompt.")
                sys.exit(1)

            prompt_filename = os.path.join(os.path.dirname(__file__), f'data/prompts/{args.prompt}.json')
            with open(prompt_filename, "r") as prompt_file:
                prompt = json.load(prompt_file)
                prompt_content += prompt["prompt_content"]

        # Option for custom prompt
        if args.prompt_text:
            prompt_content += args.prompt_text

    # Delegate to the appropriate script based on scope
    if args.scope == "image":
        #print("Generating response for image scope...")
        request, response = image_processing.process_image(args, prompt)
    elif args.scope == "text":
        #print("Generating response for text scope...")
        request, response = text_processing.process_text(args, prompt_content)
    else:
        #print("Generating response for code scope...")
        request, response = code_processing.process_code(args, prompt_content)

    # Output Responses
    if args.output == "markdown":
        # Generate a timestamp to make the file name unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create subdirectory
        assignment_directory = f"{TEST_OUTPUTS_DIRECTORY}/{args.model}"
        os.makedirs(assignment_directory, exist_ok=True)

        # Define the markdown filename
        markdown_filename = f"{assignment_directory}/{args.prompt}_{timestamp}.md"

        # Write markdown file with template
        markdown_template = load_markdown_template()
        markdown_output = markdown_template.format(
            assignment=args.assignment,
            question=args.question if args.question else "N/A",
            model=args.model,
            request=request,
            response=response,
            timestamp=timestamp
        )
        with open(markdown_filename, "w") as md_file:
            md_file.write(markdown_output)
        print(f"Markdown report saved to `{markdown_filename}`")
    elif args.output == "stdout":
        print("=== Request ===\n")
        print(request)
        print("\n=== Response ===\n")
        print(response)
    elif args.output == "direct":
        print(response)

    return 0


main()
