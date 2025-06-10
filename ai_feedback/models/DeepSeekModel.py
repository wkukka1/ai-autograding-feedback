import ollama
from pathlib import Path
from typing import Optional, Tuple
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
        submission_file: Path,
        question_num: Optional[int] = None,
        solution_file: Optional[Path] = None,
        test_output: Optional[Path] = None,
        scope: Optional[str] = None,
    ) -> Optional[Tuple[str, str]]:
        """
        Generate a model response using the prompt and assignment files.

        Args:
            prompt (str): The input prompt provided by the user.
            submission_file (Optional[Path]): The path to the submission file.
            solution_file (Optional[Path]): The path to the solution file.
            test_output (Optional[Path]): The path to the test output file.
            scope (Optional[str]): The scope to use for generating the response.
            question_num (Optional[int]): An optional question number to target specific content.

        Returns:
            Optional[Tuple[str, str]]: A tuple containing the prompt and the model's response,
                                       or None if the response was invalid.
        """

        request = f"Prompt: {prompt}"

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
