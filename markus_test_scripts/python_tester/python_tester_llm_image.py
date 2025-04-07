from dotenv import load_dotenv
import json
import re
import subprocess
import sys

        
def run_llm(model, prompt) -> str:
    """Run the LLM feedback generator and return results"""
    load_dotenv()
    llm_command = [
        sys.executable, 
        "-m", "ai_feedback",
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
    matches = re.findall(r'(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})', response)
    return [json.loads(match) for match in matches]

DEFAULT_ANNOTATION_WIDTH = 25
def convert_coordinates(coordinate_pair: list[int]) -> tuple[int]:
    return (
        coordinate_pair[0] - DEFAULT_ANNOTATION_WIDTH // 2,
        coordinate_pair[1] - DEFAULT_ANNOTATION_WIDTH // 2,
        coordinate_pair[0] + DEFAULT_ANNOTATION_WIDTH // 2,
        coordinate_pair[1] + DEFAULT_ANNOTATION_WIDTH // 2
    )
