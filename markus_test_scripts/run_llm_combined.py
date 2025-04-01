import subprocess
import pytest
import os
import os.path 
import re 
import json 

llm_feedback = ''

# Run the assignment's test file to get a test_output.txt file for model to reference
# Not used here due to token rate limitations 
def run_tests():
    result = subprocess.run(
        ["/home/docker/.autotesting/scripts/defaultvenv/bin/python", "-v", "test_bfs.py"], 
        capture_output=True, text=True, check=True
    )
    with open("test_output.txt", "w") as f:
        f.write(result.stdout)
        f.write(result.stderr)
        

def run_llm():
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "python",
        "--prompt", "code_table", # change prompt type here 
        "--scope", "code",
        "--model", "claude-3.7-sonnet", # change model type here
        "--output", "stdout",
         "--assignment", "./"
    ]

    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()
    return llm_output

def test_with_feedback(request):
    """ Generates LLM Feedback """
    # Run tests and capture output as .txt file
    # test_output_file = run_tests()

    # Run LLM feedback
    global llm_feedback 
    llm_feedback = run_llm() # get LLM feedback and display on markus
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))
        
 
def run_llm_annotation():
    # feed in previous LLM message to create annotations
    prompt = f"Previous message: {llm_feedback}."
    prompt += "These are the student mistakes you previously identified in the last message. For each of the mistakes you identified, return a JSON object containing an array of annotations, referencing the student's submission file for line and column #s. Each annotation should include: filename: The name of the student's file. content: A short description of the mistake. line_start and line_end: The line number(s) where the mistake occurs. column_start and column_end: The approximate column range of the mistake. Ensure the JSON is valid and properly formatted. Here is a sample format of the json array to return: { \"annotations\": [{\"filename\": \"student_code.py\", \"content\": \"Variable 'x' is unused.\", \"line_start\": 5, \"line_end\": 5, \"column_start\": 4, \"column_end\": 5},]}. ONLY return the json object and nothing else. Make sure the line #s don't exceed the number of lines in the file and the column #s dont exceed the range given for each line."
    llm_command = [
        "/home/docker/.autotesting/scripts/defaultvenv/bin/python", 
        "ai-autograding-feedback/main.py",
        "--submission_type", "python",
        "--prompt_text", prompt, 
        "--scope", "code",
        "--model", "claude-3.7-sonnet",
        "--output", "direct",
        "--assignment", "./"
    ]

    llm_result = subprocess.run(llm_command, capture_output=True, text=True)
    llm_output = llm_result.stdout.strip()
    return llm_output

def test_with_annotations(request):
    """ Generates LLM Annotations """
    # Run tests and capture output as .txt file
    # test_output_file = run_tests()

    # Run LLM feedback
    raw_annotation = run_llm_annotation() # generate annotations
    request.node.add_marker(pytest.mark.markus_message(raw_annotation))
    
    annotation = extract_json(raw_annotation) 
    
    annotations = json.loads(annotation)["annotations"]
    
    for annotation in annotations:
        filename = annotation["filename"]
        content = annotation["content"]
        line_start = annotation["line_start"]
        line_end = annotation["line_end"]
        column_start = annotation["column_start"]
        column_end = annotation["column_end"]

        # Convert filename to relative path
        rel_filename = os.path.relpath(filename, os.getcwd())

        # Add pytest marker for each annotation separately
        request.node.add_marker(pytest.mark.markus_annotation(
            filename=rel_filename,
            content=content,
            line_start=line_start,
            line_end=line_end,
            column_start=column_start,
            column_end=column_end,
        ))

def extract_json(text):
    """Extracts the JSON object containing 'annotations' from the model's output."""
    match = re.search(r'(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})', text)
    if not match:
        return "No valid JSON found in the response."
    
    json_str = match.group(1)  # Extract the matched JSON string
    
    try:
        return json_str
    except json.JSONDecodeError as e:
        return "Error parsing JSON."