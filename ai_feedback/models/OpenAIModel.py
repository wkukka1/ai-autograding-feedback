import os, sys
from dotenv import load_dotenv
import openai
from .Model import Model
from ..helpers.constants import INSTRUCTIONS
import PyPDF2, re

load_dotenv()

class OpenAIModel(Model):
    def __init__(self):
        super().__init__()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    """Generate a response based on the given prompt and assignment"""
    def generate_response(self, prompt, assignment_files, scope=None, question_num=None):
        if question_num:
            prompt += f' Identify and generate a response for the mistakes **only** in task {question_num}. '
            file_contents = self._get_question_contents(assignment_files, question_num)
        elif scope == "text":
            file_contents = self._get_pdf_contents(assignment_files)
        else:
            file_contents = self._get_file_contents(assignment_files)

        request = f"{INSTRUCTIONS}\n\nPrompt: {prompt}\nFiles to Reference:\n{file_contents}"

        response = self._call_openai(request)
        return request, response

    """Retrieve contents of all files and concatenate them together to attach to the prompt."""
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
        combined_content = ''
        for file_path in assignment_files:
            file_name = os.path.basename(file_path)
            pdf_content = self._extract_text_from_pdf(file_path)
            combined_content += f"{file_name}:\n{pdf_content}\n\n"

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
    
    """ Retrieve contents of files only for the specified question number.
        The format that is assumed here to extract certain code cells are very specific
        to the test files in ggr274_homework5.
    """
    def _get_question_contents(self, assignment_files, question_num):
        file_contents = ""
        task_found = False

        for file_path in assignment_files:
            # Only extract for .txt files and submission/solution files
            if not file_path.endswith(".txt") or "error_output" in file_path or file_path.endswith(".DS_Store") :
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

            # Append file name and extracted content
            file_contents += f"\n\n---\n### {file_path}\n\n"
            file_contents += intro_content + "\n\n" if intro_content else ""
            file_contents += task_content + "\n\n"

        if not task_found:
            print(f"Task {question_num} not found in any assignment file.")
            sys.exit(1)

        return file_contents.strip()

    """Send prompt to OpenAI and retrieve the response"""
    def _call_openai(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": INSTRUCTIONS},
                      {"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.5
        )
        return response.choices[0].message.content