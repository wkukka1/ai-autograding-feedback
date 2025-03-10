from ollama import chat, ChatResponse, Message, Image
from helpers.image_extractor import extract_images
from helpers.image_reader import *

def process_image(args, prompt):
    OUTPUT_DIRECTORY = "output_images"
    extract_images(args.assignment, OUTPUT_DIRECTORY)
    message = Message(
        role="user",
        content=prompt["prompt_content"],
        images=[]
    )

    # Attachments
    if prompt.get("include_question_context", False):
        context = read_question_context(OUTPUT_DIRECTORY, args.question)
        message.content = message.content.replace("{context}", "```\n" + context + "\n```")
    if prompt.get("include_submission_image", False):
        submission_image_paths = read_submission_images(OUTPUT_DIRECTORY, args.question)
        submission_image_path = submission_image_paths[0]
        message.images.append(Image(value=submission_image_path))
    if prompt.get("include_solution_image", False):
        solution_image_paths = read_solution_images(OUTPUT_DIRECTORY, args.question)
        solution_image_path = solution_image_paths[0]
        message.images.append(Image(value=solution_image_path))

    request = f"{message.content}\n{str(message.images)}\n"
    response = chat(model=args.model, messages=[message]).message.content
    return request, response