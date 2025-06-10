import os
from dotenv import load_dotenv
import anthropic
from typing import Optional, Tuple

from pathlib import Path

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
            submission_file: Path,
            solution_file: Optional[Path] = None,
            scope: Optional[str] = None,
            question_num: Optional[int] = None,
            test_output: Optional[Path] = None,
    ) -> Optional[Tuple[str, str]]:
        """
        Generates a response from Claude using the provided prompt and assignment file context.

        Args:
            prompt (str): The user's prompt for the model.
            solution_file: path to the solution file.
            submission_file: path to the submission file.
            test_output: path to the file containing the results of tests run on user submission
            scope (Optional[str]): The content scope.
            question_num (Optional[int]): Specific task number to extract from text files.

        Returns:
            Optional[Tuple[str, str]]: The original prompt and the model's response, or None if the response is invalid.
        """
        request = ""

        if question_num:
            request += f" Identify and generate a response for the mistakes **only** in question/task ${question_num}. "

        request += f"Prompt: {prompt}"

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
