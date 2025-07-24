import os
from pathlib import Path
from typing import Optional, Tuple

import anthropic
from dotenv import load_dotenv

from .Model import Model

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
        system_instructions: str,
        solution_file: Optional[Path] = None,
        scope: Optional[str] = None,
        question_num: Optional[int] = None,
        test_output: Optional[Path] = None,
        llama_mode: Optional[str] = None,
        json_schema: Optional[str] = None,
        hyperparams: Optional[dict] = None,
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
            system_instructions (str): instructions for the model
            llama_mode (Optional[str]): Optional mode to invoke llama.cpp in.
            json_schema (Optional[str]): Optional json schema to use.
            hyperparams (Optional[dict]): Optional hyperparams to use.

        Returns:
            Optional[Tuple[str, str]]: The original prompt and the model's response, or None if the response is invalid.
        """
        request = ""

        if question_num:
            request += f" Identify and generate a response for the mistakes **only** in question/task ${question_num}. "

        request += prompt

        # Set defaults and override with hyperparams if provided
        hyperparams = hyperparams or {}
        max_tokens = int(hyperparams.get("max_tokens", 1000))
        temperature = float(hyperparams.get("temperature", 0.5))
        top_p = hyperparams.get("top_p")
        stop_sequences = hyperparams.get("stop_sequences")
        metadata = hyperparams.get("metadata")
        tools = hyperparams.get("tools")
        tool_choice = hyperparams.get("tool_choice")
        stream = hyperparams.get("stream", False)

        # Normalize stop_sequences if it's a comma-separated string
        if isinstance(stop_sequences, str):
            stop_sequences = [s.strip() for s in stop_sequences.split(",") if s.strip()]

        # Construct request parameters
        request_kwargs = {
            "model": "claude-3-7-sonnet-20250219",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_instructions,
            "messages": [{"role": "user", "content": request}],
        }

        # Optional params (only add if explicitly given)
        if top_p is not None:
            request_kwargs["top_p"] = float(top_p)
        if stop_sequences:
            request_kwargs["stop_sequences"] = stop_sequences
        if metadata:
            request_kwargs["metadata"] = metadata
        if tools:
            request_kwargs["tools"] = tools
        if tool_choice:
            request_kwargs["tool_choice"] = tool_choice
        if stream:
            request_kwargs["stream"] = True

        response = self.client.messages.create(**request_kwargs)

        if not response or not response.content:
            print("Error: Invalid or empty response from Claude.")
            return None

        return prompt, response.content[0].text
