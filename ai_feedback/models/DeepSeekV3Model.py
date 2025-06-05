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
        cmd = [
            "./llama-cli",
            "-m", self.model_path,
            "--n-gpu-layers", self.gpu_layers,
            "-p", f"'prompt'" # need to add quotes to the prompt since it is multiline
        ]

        print(f"Working directory: {self.llama_bin_path}", file=sys.stdout, flush=True)
        print(f"Full command: {' '.join(cmd)}", file=sys.stdout, flush=True)

        try:
            print(f"Prompt: {prompt}")
            completed = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                cwd=self.llama_bin_path,
                timeout=120
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

        stdout_content = completed.stdout
        stderr_content = completed.stderr

        # Print both streams to help with debugging
        print("=== llama-cli stdout ===", file=sys.stdout, flush=True)
        print(stdout_content, file=sys.stdout, flush=True)
        print("=== llama-cli stderr ===", file=sys.stdout, flush=True)
        print(stderr_content, file=sys.stdout, flush=True)

        # Strip any trailing whitespace from the generated text
        generated_response = stdout_content.strip()
        return prompt, generated_response
