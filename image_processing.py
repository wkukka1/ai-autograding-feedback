import base64

from ollama import chat, Message, Image
from openai import OpenAI
from helpers.arg_options import Models
from helpers.constants import TEST_ASSIGNMENT_DIRECTORY
from helpers.image_extractor import extract_images
from helpers.image_reader import *

client = OpenAI()

def encode_image(image_path: os.PathLike):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def openai_call(message: Message, model: str):
    images = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{encode_image(image.value)}"}
        } for image in message.images
    ]
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message.content,
                    }
                ] + images,
            }
        ],
        n=1
    )
    return completion.choices[0].message.content

def process_image(args, prompt):
    OUTPUT_DIRECTORY = "output_images"
    extract_images(f"{TEST_ASSIGNMENT_DIRECTORY}/{args.assignment}/student_submission.ipynb", OUTPUT_DIRECTORY)
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
    if args.model == Models.OPENAI:
        response = openai_call(message, model="gpt-4o")
    else:
        response = chat(model=args.model, messages=[message]).message.content
    return request, response