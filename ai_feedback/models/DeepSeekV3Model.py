import subprocess
import sys
from typing import List, Optional, Tuple

from .Model import Model

class DeepseekV3Model(Model):
    def __init__(self):
        super().__init__()
        self.llama_bin_path = '/data1/llama.cpp/bin'
        self.model_path = '/data1/GGUF/DeepSeek-V3-0324-UD-Q2_K_XL/DeepSeek-V3-0324-UD-Q2_K_XL.gguf'
        self.gpu_layers = '40'

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
            Optional[Tuple[str, str]]: A tuple containing the model response or None if the response was invalid.

        """
        # Need to add quotes to the prompt since prompts are multiline
        quoted_prompt = f"'{prompt}'"

        cmd = [
            "./llama-cli",
            "-m", self.model_path,
            "--n-gpu-layers", self.gpu_layers,
            "-no-cnv",
            "-p", quoted_prompt
        ]

        try:
            completed = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.llama_bin_path,
                timeout=300
            )
        except subprocess.TimeoutExpired as e:
            # If the process hangs for more than 2 mins, print whatever has been captured so far
            print("ERROR: llama-cli timed out after 2 min.", file=sys.stdout, flush=True)
            print("Partial stdout:", e.stdout, file=sys.stdout, flush=True)
            print("Partial stderr:", e.stderr, file=sys.stdout, flush=True)
            raise
        except subprocess.CalledProcessError as e:
            # If llama-cli returns a non-zero exit code, print its stdout/stderr and re-raise
            print("ERROR: llama-cli returned non-zero exit code.", file=sys.stdout, flush=True)
            print("llama-cli stdout:", e.stdout, file=sys.stdout, flush=True)
            print("llama-cli stderr:", e.stderr, file=sys.stdout, flush=True)
            raise RuntimeError(
                f"llama.cpp failed (code {e.returncode}): {e.stderr.strip()}"
            )

        # Decode with 'replace' so invalid UTF-8 bytes become U+FFFD
        stdout_text = completed.stdout.decode('utf-8', errors='replace')

        if stdout_text.startswith(quoted_prompt):
            # Remove “prompt” plus any single newline immediately after it
            remainder = stdout_text[len(quoted_prompt):]
            # If there’s a leading newline, drop it
            if remainder.startswith("\n"):
                remainder = remainder[1:]
            response = remainder.strip()
        else:
            response = stdout_text.strip()

        # DEBUG stdout
        print("=== llama-cli stdout ===", file=sys.stdout, flush=True)
        print(response, file=sys.stdout, flush=True)

        return prompt, response
