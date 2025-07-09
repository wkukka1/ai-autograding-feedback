import json
import subprocess
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SUBMISSION = BASE_DIR / "test_submissions/cnn_example/cnn_submission.py"
SOLUTION = BASE_DIR / "test_submissions/cnn_example/cnn_solution.py"
SCHEMA_PATH = BASE_DIR / "ai_feedback/data/schema/code_annotation_schema.json"


def run_cli(model_name: str) -> dict:
    command = [
        "python3",
        "-m",
        "ai_feedback",
        "--prompt",
        "code_annotation",
        "--scope",
        "code",
        "--submission",
        str(SUBMISSION),
        "--solution",
        str(SOLUTION),
        "--model",
        model_name,
        "--json_schema",
        str(SCHEMA_PATH),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"{model_name} failed: {result.stderr}"

    output = result.stdout.strip()
    json_start = output.find("{")
    assert json_start != -1, f"{model_name} output has no JSON object"

    return json.loads(output[json_start:])


def validate_json_schema(result: dict):
    assert "annotations" in result, "Missing 'annotations' key"
    assert isinstance(result["annotations"], list), "'annotations' must be a list"
    for item in result["annotations"]:
        assert isinstance(item, dict), "Each annotation must be an object"
        for key in ["filename", "content", "line_start", "line_end", "column_start", "column_end"]:
            assert key in item, f"Missing key: {key}"
            if key in ["filename", "content"]:
                assert isinstance(item[key], str), f"{key} must be a string"
            else:
                assert isinstance(item[key], int), f"{key} must be an integer"


@pytest.mark.parametrize(
    "model",
    [
        "openai",
        "openai-vector",
        "codellama:latest",
        "deepSeek-R1:70B",
        "deepSeek-v3",
    ],
)
def test_model_outputs_valid_json_schema(model):
    result = run_cli(model)
    validate_json_schema(result)
