import ollama
import os
import sys
import re
from typing import List, Optional, Tuple
from .Model import Model
from ..helpers.constants import SYSTEM_INSTRUCTIONS


class DeepSeekModel(Model):

    def __init__(self) -> None:
        """
        Initializes the DeepSeekModel with model name and system instructions.
        """
        self.model = {
            "model": "deepseek-r1:70b",
            "instructions": SYSTEM_INSTRUCTIONS,
        }

    def generate_response(
        self,
        prompt: str,
        assignment_files: List[str],
        question_num: Optional[int] = None,
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
        self, assignment_files: List[str], question_num: int
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
                not file_path.endswith(".txt")
                or "error_output" in file_path
                or file_path.endswith(".DS_Store")
            ):
                continue

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Extract Introduction block
            intro_match = re.search(
                r"(## Introduction\b.*?)(?=\n##|\Z)", content, re.DOTALL
            )
            intro_content = intro_match.group(1).strip() if intro_match else ""

            # Extract Task block
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

    def _get_file_contents(self, assignment_files: List[str]) -> str:
        """
        Retrieve the full contents of all assignment files.

        Args:
            assignment_files (List[str]): List of file paths to be read.

        Returns:
            str: Concatenated contents of all valid text files, with filenames as section headers.
        """
        file_contents = ""
        for file_path in assignment_files:
            if not file_path.endswith(".txt") or file_path.endswith(".DS_Store"):
                continue

            file_name = os.path.basename(file_path)

            try:
                with open(file_path, "r") as file:
                    content = file.read()
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")
                continue

            file_contents += f"## {file_name}\n{content}\n\n"

        return file_contents
