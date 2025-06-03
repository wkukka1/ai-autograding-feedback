import urllib.request
import json
import os
import sys
import re
from PyPDF2 import PdfReader
from pathlib import Path
from typing import List, Optional, Tuple
from .Model import Model
from ..helpers.constants import SYSTEM_INSTRUCTIONS
from dotenv import load_dotenv


class RemoteModel(Model):
    """A class representing a remote model for generating responses.

    Currently is tied to ai_server (https://github.com/MarkUsProject/ai-server).
    """
    remote_url: str
    model_name: str

    def __init__(self, remote_url: str = "http://polymouth.teach.cs.toronto.edu:5000/chat", model_name: str = "deepseek-coder-v2:latest") -> None:
        """Initializes the remote model with a remote URL and model name.
        """
        self.remote_url = remote_url
        self.model_name = model_name

    def generate_response(
        self,
        prompt: str,
        submission_file: Path,
        solution_file: Optional[Path] = None,
        question_num: Optional[int] = None,
        test_output:Optional[Path] = None,
        scope: Optional[str] = None,
    ) -> Optional[Tuple[str, str]]:
        """
        Generate a model response using the prompt and assignment files.

        Args:
            prompt (str): The input prompt provided by the user.
            assignment_files (List[str]): A list of paths to assignment files.
            question_num (Optional[int]): An optional question number to target specific content.

        Returns:
            Optional[Tuple[str, str]]: A tuple containing the prompt and the model's response,
                                       or None if the response was invalid.
        """
        assignment_files = [f for f in (submission_file, solution_file, test_output) if f]

        if question_num:
            file_contents = self._get_question_contents(assignment_files, question_num)
        else:
            file_contents = self._get_file_contents(assignment_files)

        request = f"Prompt: {prompt}\n\nFiles to Reference:\n{file_contents}"
        load_dotenv()

        headers = {
            "X-API-KEY": os.getenv("REMOTE_API_KEY"),
            "Content-Type": "application/json"
        }
        data = {
            "content": request,
            "model": self.model_name,
        }

        # Convert the data to JSON format
        json_data = json.dumps(data).encode("utf-8")

        # Create the request
        request = urllib.request.Request(self.remote_url, data=json_data, headers=headers, method="POST")
        # Send the request and get the response
        with urllib.request.urlopen(request) as response:
            # Print the status code and response data
            print(response.status)
            response = json.loads(response.read().decode())

        return request, response

    def _get_question_contents(
        self, assignment_files: List[Path], question_num: int
    ) -> str:
        """
        Retrieve contents of files specifically for a targeted question number.

        Assumes files follow a specific markdown-like structure with sections titled
        '## Introduction' and '## Task {question_num}'.

        Args:
            assignment_files (List[str]): List of file paths.
            question_num (int): The question number to extract from files.

        Returns:
            str: Extracted content relevant to the specified question.
        """
        file_contents = ""
        task_found = False

        for file_path in assignment_files:
            if (
                "error_output" in file_path.name
                or file_path.suffix == ".DS_Store"
            ):
                continue

            text = _extract_text_from_file(file_path)
            intro_re = re.compile(r"(## Introduction\b.*?)(?=\n##|\Z)", re.DOTALL)
            task_re = re.compile(rf"(## Task {question_num}\b.*?)(?=\n##|\Z)", re.DOTALL)

            # Extract Introduction block
            intro = intro_re.search(text)
            task = task_re.search(text)
            if task:
                task_found = True

            file_contents += f"\n\n---\n### {file_path.name}\n\n"
            if intro:
                file_contents += intro.group(1).strip() + "\n\n"
            if task:
                file_contents += task.group(1).strip() + "\n\n"

        if not task_found:
            print(f"Task {question_num} not found in any provided file.")
            sys.exit(1)
        print(f"QUESTION CONTENTS : {file_contents}")
        return file_contents.strip()

    def _get_file_contents(self, assignment_files: List[Path]) -> str:
        """
        Retrieve the full contents of all assignment files.

        Args:
            assignment_files (List[str]): List of file paths to be read.

        Returns:
            str: Concatenated contents of all valid text files, with filenames as section headers.
        """
        file_contents = ""
        for file_path in assignment_files:
            if file_path.suffix == (".DS_Store"):
                continue

            file_name = os.path.basename(file_path)

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

    if ext == ".py":
        # Read Python source or plain text
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
        numbered = [
            f"(Line {i + 1}) {line.rstrip() or ''}\n"
            for i, line in enumerate(lines)
        ]
        header = f"=== {file_path.name} ===\n"
        return header + "".join(numbered)

    elif ext == ".pdf":
        # Use PyPDF2 to pull text out of each page
        reader = PdfReader(str(p))
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        return "\n\n".join(pages_text)

    elif ext == '.txt':
        return file_path.read_text(encoding="utf-8")
    else:
        raise ValueError(
            f"Unsupported file extension: {ext!r}. "
            "Use .py, .pdf, or .txt only."
        )