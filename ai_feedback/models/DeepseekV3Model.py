import subprocess
from typing import List

from pathlib import Path

from .Model import Model

class DeepseekV3Model(Model):
    def __init__(self):
        super().__init__()
        self.llama_bin_path = '/data/llama.cpp/bin'
        self.model_path = '/data1/GGUF/DeepSeek-V3-0324-UD-Q2_K_XL/DeepSeek-V3-0324-UD-Q2_K_XL.gguf'
        self.gpu_layers = '40'

    def generate_response(self, prompt: str, assignment_files: List[Path]):
        cmd = [
            self.llama_bin_path,
            "-m", self.model_path,
            "-n-gpu-layers
        ]

        try:
            completed = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"llama.cpp failed (code {e.returncode}): {e.stderr.strip()}"
            )

        raw = completed.stdout
        # If llama echoes the prompt, strip it off here. Otherwise just .strip():
        generated = raw.strip()
        return prompt, generated
