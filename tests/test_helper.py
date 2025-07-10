import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from unittest.mock import patch

import pytest

from ai_feedback.__main__ import main
from ai_feedback.models.Model import Model
from ai_feedback.models.OpenAIModel import OpenAIModel

all_prompts = []


@pytest.fixture(scope="session", autouse=True)
def collect_prompts_and_write_individual_files():
    all_prompts.clear()
    yield

    report_dir = Path("prompt_reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    for entry in report_dir.iterdir():
        if entry.is_dir() and entry.suffix == ".txt":
            shutil.rmtree(entry)

    master_index = report_dir / "index.txt"
    with open(master_index, "w", encoding="utf-8") as idx_file:
        idx_file.write(f"Prompt Log Index @ {datetime.now().isoformat()} UTC\n\n")

    for count, (test_name, mock_loc, prompt_text) in enumerate(all_prompts, start=1):
        safe_test = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in test_name)
        safe_loc = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in mock_loc)

        filename = f"{count:03d}_{safe_test}_{safe_loc}.txt"
        file_path = report_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            # (Optional) include a header in each file:
            f.write(f"Test: {test_name}\n")
            f.write(f"Location: {mock_loc}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()} UTC\n")
            f.write("\n")
            f.write(prompt_text)
            f.write("\n")

        with open(master_index, "a", encoding="utf-8") as idx_file:
            idx_file.write(f"{filename}  ←  [{test_name}] at {mock_loc}\n")

    print(f"\nWritten {len(all_prompts)} prompt files into: {report_dir.resolve()}\n")


@pytest.fixture(autouse=True)
def mock_and_capture(request):
    test_name = request.node.name

    def fake_base(self, prompt, *args, **kwargs):
        all_prompts.append((test_name, "Model.generate_response", prompt))
        return prompt, prompt

    model_patch = patch.object(Model, "generate_response", side_effect=fake_base)
    model_patch.start()

    def fake_generate_response(
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
    ):
        all_prompts.append((test_name, "OpenAIModel.generate_response", prompt))
        return prompt, f"[MOCKED RESPONSE] \n {prompt}"

    openai_patch = patch.object(OpenAIModel, "generate_response", side_effect=fake_generate_response, autospec=True)
    openai_patch.start()

    class DummyMsg:
        def __init__(self, text):
            self.content = text

    class DummyReply:
        def __init__(self, text):
            self.message = DummyMsg(text)

    def fake_ip_chat(model, messages, options=None):
        text = messages[-1].content
        all_prompts.append((test_name, "image_processing.chat", text))
        return DummyReply(text)

    ip_patch = patch("ai_feedback.image_processing.chat", side_effect=fake_ip_chat)
    ip_patch.start()

    def fake_ds_chat(model, messages, **kwargs):
        text = messages[-1]["content"]
        all_prompts.append((test_name, "ollama.chat", text))
        return {"message": {"content": text}}

    ds_patch = patch("ollama.chat", side_effect=fake_ds_chat)
    ds_patch.start()

    yield

    patch.stopall()


def run_cli_and_capture(argv_list, capsys):
    """
    Helper to run the CLI with a custom sys.argv and capture stdout/stderr.
    Returns the captured stdout as a string.
    """
    orig_argv = sys.argv
    sys.argv = ["ai_feedback"] + argv_list

    try:
        main()
    finally:
        sys.argv = orig_argv

    captured = capsys.readouterr()
    return captured.out
