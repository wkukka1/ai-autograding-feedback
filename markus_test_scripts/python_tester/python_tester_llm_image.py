import json
import subprocess
import re

        
def run_llm(model, prompt) -> str:
    """Run the LLM feedback generator and return results"""
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "jupyter",
        "--prompt", prompt,
        "--scope", "image",
        "--assignment", "./",
        "--question", "Question 5b",
        "--model", model,
        "--output", "stdout"
    ]

    # Capture the output from the LLM program
    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()
    return llm_output

def extract_json(response) -> list[dict]:
    match = re.search(r"\`\`\`json([\S\s]+)\`\`\`", response)
    if match:
        return json.loads(match.group(1))
    return []

DEFAULT_ANNOTATION_WIDTH = 25
def convert_coordinates(coordinate_pair: list[int]) -> tuple[int]:
    return (
        coordinate_pair[0] - DEFAULT_ANNOTATION_WIDTH // 2,
        coordinate_pair[1] - DEFAULT_ANNOTATION_WIDTH // 2,
        coordinate_pair[0] + DEFAULT_ANNOTATION_WIDTH // 2,
        coordinate_pair[1] + DEFAULT_ANNOTATION_WIDTH // 2
    )
