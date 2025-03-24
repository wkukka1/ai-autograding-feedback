import os
from dotenv import load_dotenv
import anthropic
import sys
from models.Model import Model
from helpers.constants import INSTRUCTIONS

# Load environment variables from .env file
load_dotenv()

class ClaudeModel(Model):
    def __init__(self):
        super().__init__()
        
        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    """Generate a response based on the given prompt and assignment"""
    def generate_response(self, prompt, assignment_files, question_num=None):
        request = ''
    
        if question_num:
            request = request + f' Identify and generate a response for the mistakes **only** in question/task ${question_num}. '
            file_contents = self._get_question_contents(assignment_files, question_num)
        else:
            file_contents = self._get_file_contents(assignment_files)
        
        # Combine the model's instructions and the files to reference in the full prompt
        request = request + f"Prompt: {prompt}\n\nFiles to Reference:\n{file_contents}"
        
        response = self.client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            temperature=0.5,
            system=INSTRUCTIONS,
            
            messages=[
                {
                    "role": "user",
                    "content": request
                }
            ]
        )
        if not response or not response.content:
            print("Error: Invalid or empty response from Ollama.")
            return None
        
        return prompt, response.content[0].text 
    
    
    """ Retrieve contents of all files and concatenate them together to attach to the prompt. """
    def _get_file_contents(self, assignment_files):
        file_contents = ""
        for file_path in assignment_files:
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
            file_contents += f"## {file_name}\n{content}\n\n"
        return file_contents
        
