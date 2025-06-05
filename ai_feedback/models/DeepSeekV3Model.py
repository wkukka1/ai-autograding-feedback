import socket
import subprocess
import sys
import requests
import time
from typing import List, Optional, Tuple

from pathlib import Path

from .Model import Model

class DeepseekV3Model(Model):
    def __init__(self):
        super().__init__()
        self.server_port = 8080
        self.llama_bin_path = '/data1/llama.cpp/bin'
        self.llama_server_path = '/data1/GGUF'
        self.model_path = '/data1/GGUF/DeepSeek-V3-0324-UD-Q2_K_XL/DeepSeek-V3-0324-UD-Q2_K_XL.gguf'
        self.gpu_layers = '40'
        self.server_host = '127.0.0.1'

    def generate_response(
        self,
        prompt: str,
        submission_file: Path,
        mode: Optional[str],
        solution_file: Optional[Path] = None,
        scope: Optional[str] = None,
        question_num: Optional[int] = None,
        test_output: Optional[Path] = None,
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
        if mode == 'server':
            response = self.get_response_server(prompt)
        else:
            prompt = f"'{prompt}'"
            response = self.get_response_cli(prompt)

        # Remove prompt from response
        if response.startswith(prompt):
            tail = response[len(prompt):]
            if tail.startswith("\n"):
                tail = tail[1:]
            response = tail

        response = response.strip()

        # Remove end of response marker
        end_marker = "[end of text]"
        if response.endswith(end_marker):
            response = response[: -len(end_marker)]
            response = response.strip()

        # DEBUG
        print(f"=== llama-{mode} returned ===", file=sys.stdout, flush=True)
        print(response, file=sys.stdout, flush=True)

        return prompt, response

    def get_response_server(
            self,
            prompt: str,
    ) -> str:
        """
        Generate a model response using the prompt

        Args:
            prompt (str): The input prompt provided by the user.

        Returns:
            str: A tuple containing the model response or None if the response was invalid.
        """

        # Check if the server is up
        server_was_running = self._is_port_open()
        server_proc = None

        if not server_was_running:
            # Not running we start it and wait for readiness
            server_proc = self._start_server()

            print(f"Waiting up to 5 minutes for llama-server to be ready...", file=sys.stdout, flush=True)
            ready = self._wait_for_server(300)
            if not ready:
                # If the server never came up, kill what we started and bail
                print("ERROR: llama-server never opened port.", file=sys.stderr, flush=True)
                self._stop_server(server_proc)
                raise RuntimeError("Failed to start llama-server within timeout.")

            print("llama-server is now listening.", file=sys.stdout, flush=True)
        else:
            print("Detected existing llama-server on port "
                  f"{self.server_port}; reusing it.", file=sys.stdout, flush=True)


        url = f"http://{self.server_host}:{self.server_port}/v1/completions"

        payload = {
            "prompt": prompt,
        }

        try:
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
        except requests.RequestException as e:
            print("ERROR: Request to llama-server failed:", str(e), file=sys.stderr, flush=True)
            if server_proc:
                self._stop_server(server_proc)
            raise

        data = response.json()

        try:
            model_output = data["choices"][0]["text"]
        except (KeyError, IndexError):
            print("ERROR: Unexpected JSON format from llama-server:", data, file=sys.stderr, flush=True)
            raise KeyError("Unexpected JSON format from llama-server.")

        if server_proc:
            self._stop_server(server_proc)
        else:
            print("Keeping existing llama-server running (we did not start it).", file=sys.stdout, flush=True)

        return model_output

    def get_response_cli(
            self,
            prompt: str,
    ) -> str:
        """
        Generate a model response using the prompt

        Args:
            prompt (str): The input prompt provided by the user.

        Returns:
            str: The model response or None if the response was invalid.
        """
        # Need to add quotes to the prompt since prompts are multiline

        cmd = [
            "./llama-cli",
            "-m", self.model_path,
            "--n-gpu-layers", self.gpu_layers,
            "-no-cnv",
            "-p", prompt
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
            # If the process hangs for more than 5 minutes, print whatever has been captured so far
            print("ERROR: llama-cli timed out after 5 minutes.", file=sys.stdout, flush=True)
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
        return completed.stdout.decode('utf-8', errors='replace')


    def _is_port_open(self) -> bool:
        """
        Used to check if llama-server is already listening.

        Returns:
              bool: True if we can open a TCP connection to (host, port) and False otherwise
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        try:
            sock.connect((self.server_host, self.server_port))
            sock.close()
            return True
        except (ConnectionRefusedError, socket.timeout):
            return False

    def _start_server(self) -> subprocess.Popen:
        """
        Launch llama-server in a subprocess and return the Popen handle.

        Returns:
            subprocess.Popen: subprocess.Popen object for the process running the server.
        """
        cmd = [
            f"{self.llama_bin_path}/llama-server",
            "-m", self.model_path,
            "--port", str(self.server_port),
            "--n-gpu-layers", self.gpu_layers,
        ]

        print(f"Starting llama-server with command: {' '.join(cmd)}", file=sys.stdout, flush=True)
        # Start it in its own process, don’t capture stdout/stderr
        server_proc = subprocess.Popen(
            cmd,
            cwd=self.llama_bin_path,
            stdout=sys.stdout,  # print server’s stdout to our terminal
            stderr=sys.stderr  # print server’s stderr to our terminal
        )
        return server_proc

    def _wait_for_server(self, timeout_s: int) -> bool:
        """
        Poll every 10 seconds until either the server returns healthy or we hit timeout.

        Returns:
            True if port became available, False if we timed out.
        """
        url = f"http://{self.server_host}:{self.server_port}/health"
        start = time.time()
        while time.time() - start < timeout_s:
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    return True
            except requests.RequestException:
                pass
            print(f"Server not ready yet; retrying in 10 seconds", file=sys.stdout, flush=True)
            time.sleep(10)
        return False

    def _stop_server(self, proc: subprocess.Popen) -> None:
        """
        Gracefully terminate the llama-server process we started.
        """
        print("Shutting down llama-server...", file=sys.stdout, flush=True)
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("llama-server did not exit in 5s; killing.", file=sys.stdout, flush=True)
            proc.kill()
            proc.wait()
