import subprocess
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
            "-p", prompt
        ]

        try:
            completed = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                cwd=self.llama_bin_path,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"llama.cpp failed (code {e.returncode}): {e.stderr.strip()}"
            )

        raw = completed.stdout
        response = raw.strip()
        print(response)
        return prompt, response
