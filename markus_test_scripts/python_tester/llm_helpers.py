import re, json

ANNOTATION_PROMPT = """These are the student mistakes you previously identified in the 
last message. For each of the mistakes you identified, return a JSON object containing 
an array of annotations, referencing the student's submission file for line and column #s. 
Each annotation should include: filename: The name of the student's file. content: 
A short description of the mistake. line_start and line_end: The line number(s) where the
mistake occurs. Ensure the JSON is valid and properly formatted. Here is a sample format 
of the json array to return: { \"annotations\": [{\"filename\": \"student_code.py\", 
\"content\": \"Variable 'x' is unused.\", \"line_start\": 5, \"line_end\": 5,]}. 
ONLY return the json object and nothing else. Make sure the line #s don't exceed 
the number of lines in the file. You can use markdown syntax in the annotation's content,
especially when denoting code."""

def extract_json(text):
    """Extracts the JSON object containing 'annotations' from the model's output."""
    match = re.search(r'(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})', text)
    if not match:
        return "No valid JSON found in the response."
    
    json_str = match.group(1)
    
    try:
        return json_str
    except json.JSONDecodeError as e:
        return "Error parsing JSON."
    
def add_annotation_columns(annotations, submission):
    """
    Given LLM annotations with line_start and line_end, add 
    column_start and column_end metadata to the JSON object. 
    """
    try:
        file_path = submission.__file__
        with open(file_path, 'r') as file:
            file_lines = file.readlines()
    except Exception as e:
        print(f"Error reading submission file: {e}")
    
    annotations_with_columns = []

    for annotation in annotations:
        filename = annotation["filename"]
        line_start = annotation["line_start"]
        line_end = annotation["line_end"]

        if not file_lines or line_start > len(file_lines) or line_end > len(file_lines):
            print(f"Skipping invalid line numbers for {filename}: {line_start}-{line_end}")
            continue

        column_starts = []
        column_ends = []

        for i in range(line_start - 1, line_end):
            if i >= len(file_lines):
                continue

            line = file_lines[i]
            stripped_line = line.rstrip("\n")

            if stripped_line.strip(): # find start and end of each line
                start_col = len(line) - len(line.lstrip())
                end_col = len(stripped_line)
            else:
                start_col = 0
                end_col = 1

            column_starts.append(start_col)
            column_ends.append(end_col)

        if column_starts and column_ends:
            # find min and max columns if multiline annotation
            column_start = min(column_starts)
            column_end = max(column_ends)
        else:
            column_start = 0
            column_end = 1


        annotation["column_start"] = column_start
        annotation["column_end"] = column_end
        annotations_with_columns.append(annotation)

    return annotations_with_columns