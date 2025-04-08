import os
from dotenv import load_dotenv
import anthropic
from .Model import Model
from ..helpers.constants import INSTRUCTIONS
import PyPDF2

# Load environment variables from .env file
load_dotenv()

class ClaudeModel(Model):
    def __init__(self):
        super().__init__()

        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    """Generate a response based on the given prompt and assignment"""
    def generate_response(self, prompt, assignment_files, scope=None, question_num=None):
        request = ''

        if question_num:
            request = request + f' Identify and generate a response for the mistakes **only** in question/task ${question_num}. '
            file_contents = self._get_question_contents(assignment_files, question_num)
        elif scope == "text":
            file_contents = self._get_pdf_contents(assignment_files)
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
            file_name = os.path.basename(file_path)
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")
                continue

            file_contents += f"=== {file_name} ===\n"

            for i, line in enumerate(lines, start=1):
                stripped_line = line.rstrip("\n")

                if stripped_line.strip():
                    file_contents += f"(Line {i}) {stripped_line}\n"
                else:
                    file_contents += f"(Line {i}) {line}"  # Keep blank lines for readability

            file_contents += "\n"

        return file_contents
    
    def _get_pdf_contents(self, assignment_files: list) -> str:
        for file_path in assignment_files:
            if "student_pdf_submission.pdf" in file_path:
                student_pdf_content = self._extract_text_from_pdf(file_path)
            elif "instructor_pdf_solution.pdf" in file_path:
                instructor_pdf_content = self._extract_text_from_pdf(file_path)

        combined_content = f"student_pdf_submission.pdf:\n{student_pdf_content}\n\ninstructor_pdf_solution.pdf:\n{instructor_pdf_content}"

        return combined_content

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract and clean text content from a PDF file."""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(reader.pages):
                raw_text = page.extract_text()
                if not raw_text:
                    continue

                cleaned_text = raw_text.strip()
                text += f"Page {page_num}:\n{cleaned_text}\n\n"

        return text

