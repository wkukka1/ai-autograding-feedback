import ollama
import os, sys
import re 
from models.Model import Model
from helpers.constants import INSTRUCTIONS

class DeepSeekModel(Model):
    def __init__(self):
        # Initialize the model configuration
        self.model = {
            "name": "Markus LLM Assistant",
            "model": "deepseek-r1:70b",
            "instructions": (
               INSTRUCTIONS
            ),
        }

    def generate_response(self, prompt, assignment_files, question_num=None):
    
        if question_num: 
            file_contents = self._get_question_contents(assignment_files, question_num)
        else:
            file_contents = self._get_file_contents(assignment_files)
        
        # Combine the model's instructions and the files to reference in the full prompt
        request = f"{self.model['instructions']}\n\nPrompt: {prompt}\n\nFiles to Reference:\n{file_contents}"

        response = ollama.chat(model=self.model["model"], messages=[{"role": "user", "content": request}])
        
        if not response or "message" not in response or "content" not in response["message"]:
            print("Error: Invalid or empty response from Ollama.")
            return None
        
        return request, response["message"]["content"]
    
    """ Retrieve contents of files only for the specified question number.
        The format that is assumed here to extract certain code cells are very specific
        to the test files in ggr274_homework5.
    """
    def _get_question_contents(self, assignment_files, question_num):
        file_contents = ""
        task_found = False 

        for file_path in assignment_files:
            # Only extract for .txt files and submission/solution files 
            if not file_path.endswith(".txt") or "error_output" in file_path or file_path.endswith(".DS_Store"):
                continue
    
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Extract Introduction block
            intro_match = re.search(r"(## Introduction\b.*?)(?=\n##|\Z)", content, re.DOTALL)
            intro_content = intro_match.group(1).strip() if intro_match else ""

            # Extract Task block
            task_pattern = rf"(## Task {question_num}\b.*?)(?=\n##|\Z)"
            task_match = re.search(task_pattern, content, re.DOTALL)

            if task_match:
                task_content = task_match.group(1).strip()
                task_found = True
            else:
                task_content = f"Error: Task {question_num} not found in {file_path}."

            # Append file name and extracted content
            file_contents += f"\n\n---\n### {file_path}\n\n"
            file_contents += intro_content + "\n\n" if intro_content else ""
            file_contents += task_content + "\n\n"

        if not task_found:
            print(f"Task {question_num} not found in any assignment file.")
            sys.exit(1)
        return file_contents.strip()
    
    """ Retrieve contents of all files and concatenate them together to attach to the prompt. """
    def _get_file_contents(self, assignment_files):
        file_contents = ""
        for file_path in assignment_files:
            if not file_path.endswith(".txt") or file_path.endswith(".DS_Store"):
                continue
            # Get the filename from the file path
            file_name = os.path.basename(file_path)

            # Read the content of the file
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")
                continue
            
            # Prepend the filename and append the content
            file_contents += f"### {file_name}\n{content}\n\n"
        return file_contents
        
