import os
import sys
import re
from dotenv import load_dotenv
import anthropic
import PyPDF2
from typing import List, Optional, Tuple, Union

from .Model import Model
from ..helpers.constants import SYSTEM_INSTRUCTIONS

# Load environment variables from .env file
load_dotenv()


class ClaudeModel(Model):
    def __init__(self) -> None:
        """
        Initializes the ClaudeModel with the Anthropic client using an API key.
        """
        super().__init__()
        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    def generate_response(
        self,
        prompt: str,
        assignment_files: List[str],
        scope: Optional[str] = None,
        question_num: Optional[int] = None,
    ) -> Optional[Tuple[str, str]]:
        """
        Generates a response from Claude using the provided prompt and assignment file context.

        Args:
            prompt (str): The user's prompt for the model.
            assignment_files (List[str]): A list of file paths relevant to the assignment.
            scope (Optional[str]): The content scope.
            question_num (Optional[int]): Specific task number to extract from text files.

        Returns:
            Optional[Tuple[str, str]]: The original prompt and the model's response, or None if the response is invalid.
        """
        request = ""

        if question_num:
            request += f" Identify and generate a response for the mistakes **only** in question/task ${question_num}. "
            file_contents = self._get_question_contents(assignment_files, question_num)
        elif scope == "text":
            file_contents = self._get_pdf_contents(assignment_files)
        else:
            file_contents = self._get_file_contents(assignment_files)

        request += f"Prompt: {prompt}\n\nFiles to Reference:\n{file_contents}"

        response = self.client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            temperature=0.5,
            system=SYSTEM_INSTRUCTIONS,
            messages=[{"role": "user", "content": request}],
        )

        if not response or not response.content:
            print("Error: Invalid or empty response from Claude.")
            return None

        return prompt, response.content[0].text

    def _get_file_contents(self, assignment_files: List[str]) -> str:
        """
        Retrieves contents of all files and concatenates them with line numbers.

        Args:
            assignment_files (List[str]): A list of assignment file paths.

        Returns:
            str: Combined, formatted content of the files with line numbers.
        """
        file_contents = ""

        for file_path in assignment_files:
            file_name = os.path.basename(file_path)

            try:
                with open(file_path, "r") as file:
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
                    file_contents += (
                        f"(Line {i}) {line}"  # Keep blank lines for readability
                    )

            file_contents += "\n"

        return file_contents

    def _get_pdf_contents(self, assignment_files: List[str]) -> str:
        """
        Retrieves text content from PDF files specifically for student and instructor submissions.

        Args:
            assignment_files (List[str]): A list of assignment file paths.

        Returns:
            str: Combined content of student and instructor PDFs.
        """
        student_pdf_content = ""
        instructor_pdf_content = ""

        for file_path in assignment_files:
            if "student_pdf_submission.pdf" in file_path:
                student_pdf_content = self._extract_text_from_pdf(file_path)
            elif "instructor_pdf_solution.pdf" in file_path:
                instructor_pdf_content = self._extract_text_from_pdf(file_path)

        combined_content = (
            f"student_pdf_submission.pdf:\n{student_pdf_content}\n\n"
            f"instructor_pdf_solution.pdf:\n{instructor_pdf_content}"
        )

        return combined_content

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extracts and formats text from a PDF file, page by page.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: Text content extracted from the PDF.
        """
        text = ""

        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                raw_text = page.extract_text()
                if not raw_text:
                    continue

                cleaned_text = raw_text.strip()
                text += f"Page {page_num}:\n{cleaned_text}\n\n"

        return text

    def _get_question_contents(
        self, assignment_files: List[str], question_num: int
    ) -> str:
        """
        Retrieves content related to a specific question number from assignment files.

        Args:
            assignment_files (List[str]): A list of assignment file paths.
            question_num (int): The task number to extract content for.

        Returns:
            str: Combined content of introduction and matching tasks across relevant files.

        Raises:
            SystemExit: If the specified task number is not found in any file.
        """
        file_contents = ""
        task_found = False

        for file_path in assignment_files:
            if (
                not file_path.endswith(".txt")
                or "error_output" in file_path
                or file_path.endswith(".DS_Store")
            ):
                continue

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            intro_match = re.search(
                r"(## Introduction\b.*?)(?=\n##|\Z)", content, re.DOTALL
            )
            intro_content = intro_match.group(1).strip() if intro_match else ""

            task_pattern = rf"(## Task {question_num}\b.*?)(?=\n##|\Z)"
            task_match = re.search(task_pattern, content, re.DOTALL)

            task_content = ""
            if task_match:
                task_content = task_match.group(1).strip()
                task_found = True

            file_contents += f"\n\n---\n### {file_path}\n\n"
            file_contents += intro_content + "\n\n" if intro_content else ""
            file_contents += task_content + "\n\n"

        if not task_found:
            print(f"Task {question_num} not found in any assignment file.")
            sys.exit(1)

        return file_contents.strip()
