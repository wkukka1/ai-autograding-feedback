import ollama
import os
import sys
import re
from pathlib import Path
from typing import List, Optional, Tuple

from PyPDF2 import PdfReader

from .Model import Model
from ..helpers.constants import SYSTEM_INSTRUCTIONS


class CodeLlamaModel(Model):

    def __init__(self) -> None:
        """
        Initializes the CodeLlamaModel with configuration for the model and system instructions.
        """
        self.model = {
            "model": "codellama:latest",
            "instructions": SYSTEM_INSTRUCTIONS,
        }

    def generate_response(
        self,
        prompt: str,
        submission_file: Path,
        question_num: Optional[int] = None,
        solution_file: Optional[Path] = None,
        test_output: Optional[Path] = None,
        scope: Optional[str] = None,
    ) -> Optional[Tuple[str, str]]:
        """
        Generates a response from the CodeLlama model using the provided prompt
        and assignment file contents.

        Args:
            prompt (str): The user's prompt to be fed into the model.
            assignment_files (List[str]): A list of assignment file paths.
            question_num (Optional[int]): An optional specific question number to extract content for.

        Returns:
            Optional[Tuple[str, str]]: A tuple of the request and the model's response,
                                       or None if no valid response is returned.
        """
        assignment_files = [f for f in (submission_file, solution_file, test_output) if f]

        if question_num:
            file_contents = self._get_question_contents(assignment_files, question_num)
        else:
            file_contents = self._get_file_contents(assignment_files)

        request = f"Prompt: {prompt}\n\nFiles to Reference:\n{file_contents}"
        response = ollama.chat(
            model=self.model["model"],
            messages=[
                {"role": "system", "content": self.model["instructions"]},
                {"role": "user", "content": request},
            ],
        )

        if (
            not response
            or "message" not in response
            or "content" not in response["message"]
        ):
            print("Error: Invalid or empty response from Ollama.")
            return None

        return request, response["message"]["content"]

    def _get_question_contents(
        self, assignment_files: List[Path], question_num: int
    ) -> str:
        """
        Retrieve contents of files specifically for a targeted question number.

        Assumes files follow a specific markdown-like structure with sections titled
        '## Introduction' and '## Task {question_num}'.

        Args:
            assignment_files (List[str]): List of file paths to parse.
            question_num (int): The target task number to extract.

        Returns:
            str: Combined content of the introduction and the specified task from matching files.

        Raises:
            SystemExit: If no matching task is found in the provided files.
        """
        file_contents = ""
        task_found = False

        for file_path in assignment_files:
            if (
                "error_output" in file_path.name
                or file_path.suffix == ".DS_Store"
            ):
                continue

            content = file_path.read_text()

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

    def _get_file_contents(self, assignment_files: List[Path]) -> str:
        """
        Retrieves and concatenates the contents of all assignment files.

        Args:
            assignment_files (List[str]): A list of file paths.

        Returns:
            str: Combined file contents, each prefixed with its filename as a Markdown header.
        """
        file_contents = ""
        for file_path in assignment_files:
            if file_path.suffix == ".DS_Store":
                continue

            file_name = file_path.name

            try:
                content = _extract_text_from_file(file_path)
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")
                continue

            file_contents += f"## {file_name}\n{content}\n\n"

        return file_contents

def _extract_text_from_file(file_path: Path) -> str:
    """
    Given a path to a .py, .pdf, or .txt file, return its text content.
    Raises ValueError for unsupported extensions.
    """
    p = Path(file_path)
    ext = p.suffix.lower()

    if ext == ".py" or ext == ".txt":
        # Read Python source or plain text
        return p.read_text(encoding="utf-8")

    elif ext == ".pdf":
        # Use PyPDF2 to pull text out of each page
        reader = PdfReader(str(p))
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        return "\n\n".join(pages_text)

    else:
        raise ValueError(
            f"Unsupported file extension: {ext!r}. "
            "Use .py, .pdf, or .txt only."
        )