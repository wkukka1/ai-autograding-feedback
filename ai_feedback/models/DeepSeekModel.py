import json
from pathlib import Path
from typing import Optional, Tuple

import ollama

from .Model import Model


class DeepSeekModel(Model):

    def __init__(self) -> None:
        """
        Initializes the DeepSeekModel with model name and system instructions.
        """
        self.model = {"model": "deepseek-r1:70b"}

    def generate_response(
        self,
        prompt: str,
        submission_file: Path,
        system_instructions: str,
        question_num: Optional[int] = None,
        solution_file: Optional[Path] = None,
        test_output: Optional[Path] = None,
        scope: Optional[str] = None,
        llama_mode: Optional[str] = None,
        json_schema: Optional[str] = None,
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
            system_instructions (str): instructions for the model
            llama_mode (Optional[str]): Optional mode to invoke llama.cpp in.
            json_schema (Optional[str]): Optional json schema to use.

        Returns:
            Optional[Tuple[str, str]]: A tuple containing the prompt and the model's response,
                                       or None if the response was invalid.
        """
        if json_schema:
            schema_path = Path(json_schema)
            if not schema_path.exists():
                raise FileNotFoundError(f"JSON schema file not found: {schema_path}")
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
        else:
            schema = None

        response = ollama.chat(
            model=self.model["model"],
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt},
            ],
            format=schema['schema'] if schema else None,
        )

        if not response or "message" not in response or "content" not in response["message"]:
            print("Error: Invalid or empty response from Ollama.")
            return None

        return prompt, response["message"]["content"]
