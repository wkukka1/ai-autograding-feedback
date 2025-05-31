import os
import sys
import re
from pathlib import Path
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
        submission_file: str,
        solution_file: str,
        scope: Optional[str] = None,
        question_num: Optional[int] = None,
    ) -> Optional[Tuple[str, str]]:
        """
        Generates a response from Claude using the provided prompt and assignment file context.

        Args:
            prompt (str): The user's prompt for the model.
            solution_file: path to the solution file.
            submission_file: path to the submission file.
            scope (Optional[str]): The content scope.
            question_num (Optional[int]): Specific task number to extract from text files.

        Returns:
            Optional[Tuple[str, str]]: The original prompt and the model's response, or None if the response is invalid.
        """
        request = ""
        submission = Path(submission_file)
        solution = Path(solution_file) if solution_file else None

        if question_num:
            contents = self._get_question_contents(submission, "Submission", question_num) + "\n\n"
            if solution:
                contents += self._get_question_contents(solution, "Solution", question_num)

        elif scope == "text":
            contents = self._get_pdf_contents(submission, "Submission", solution, "Solution")
        else:
            contents = self._get_file_contents(submission, "Submission")
            if solution:
                contents += "\n\n" + self._get_file_contents(solution, "Solution")

        request = f"Prompt: {prompt}\n\nFiles to reference:\n{contents}"

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


    def _get_file_contents(self, file_path: Path, label: str) -> str:
        """Read any text file and number its lines, with a labeled header."""
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
        numbered = [
            f"(Line {i+1}) {line.rstrip() or ''}\n"
            for i, line in enumerate(lines)
        ]
        header = f"=== {label}: {file_path.name} ===\n"
        return header + "".join(numbered)

    def _get_pdf_contents(
        self,
        sub_path: Path,
        sub_label: str,
        sol_path: Optional[Path],
        sol_label: str,
    ) -> str:
        """Extract text from one or two PDFs, with labeled sections."""
        student_txt = self._extract_text_from_pdf(sub_path)
        result = f"{sub_label} PDF ({sub_path.name}):\n{student_txt}"
        if sol_path:
            instructor_txt = self._extract_text_from_pdf(sol_path)
            result += (
                f"\n\n{sol_label} PDF ({sol_path.name}):\n{instructor_txt}"
            )
        return result

    def _get_question_contents(
        self,
        file_path: Path,
        label: str,
        question_num: int,
    ) -> str:
        """Extract only the Introduction and Task #{question_num} from a text file."""
        text = file_path.read_text(encoding="utf-8")

        intro_re = re.compile(r"(## Introduction\b.*?)(?=\n##|\Z)", re.DOTALL)
        task_re  = re.compile(rf"(## Task {question_num}\b.*?)(?=\n##|\Z)", re.DOTALL)

        intro_match = intro_re.search(text)
        task_match  = task_re.search(text)
        if not task_match:
            print(f"Task {question_num} not found in {file_path.name}.")
            sys.exit(1)

        parts = []
        if intro_match:
            parts.append(intro_match.group(1).strip())
        parts.append(task_match.group(1).strip())

        header = f"=== {label}: {file_path.name} ===\n"
        return header + "\n\n".join(parts)

    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract and concatenate text from each page of a PDF."""
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(reader.pages):
                raw = page.extract_text()
                if not raw:
                    continue
                text += f"Page {page_num}:\n{raw.strip()}\n\n"
        return text