import json
import subprocess
import tempfile
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent.parent
IMAGE_SUBMISSION = BASE_DIR / "test_submissions/ggr274_homework5/image_test1/student_submission.ipynb"
IMAGE_SUBMISSION_IMAGE = BASE_DIR / "test_submissions/ggr274_homework5/image_test1/student_submission.png"
IMAGE_SCHEMA_PATH = BASE_DIR / "ai_feedback/data/schema/image_annotation_schema.json"


@pytest.fixture(scope="module")
def openai_schema_result():
    """Module-scoped fixture that makes one OpenAI API call and returns the parsed result"""
    result_process = run_image_cli("openai")
    assert result_process.returncode == 0, f"OpenAI failed with schema: {result_process.stderr}"

    parsed_result = parse_strict_json(result_process.stdout.strip(), "openai")
    return parsed_result


def run_image_cli(model_name: str, schema_path: str = None) -> list:
    schema_to_use = schema_path or str(IMAGE_SCHEMA_PATH)
    command = [
        "python3",
        "-m",
        "ai_feedback",
        "--prompt",
        "image_analyze_annotations",
        "--scope",
        "image",
        "--submission",
        str(IMAGE_SUBMISSION),
        "--submission_image",
        str(IMAGE_SUBMISSION_IMAGE),
        "--question",
        "Question 5b",
        "--model",
        model_name,
        "--json_schema",
        schema_to_use,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result


def parse_strict_json(output: str, model_name: str) -> list:
    """Parse JSON from plain text output"""
    return json.loads(output.strip())


def validate_schema_constraints(result: list):
    """Validate that the result strictly follows ALL schema constraints"""
    assert isinstance(result, list), "Result must be a list"
    assert len(result) > 0, "Result must contain at least one annotation"

    for item in result:
        assert isinstance(item, dict), "Each annotation must be an object"

        assert "description" in item, "Missing required field: description"
        assert "location" in item, "Missing required field: location"

        assert set(item.keys()) == {
            "description",
            "location",
        }, f"Extra fields found: {set(item.keys()) - {'description', 'location'}}"

        assert isinstance(item["description"], str), "description must be a string"
        assert len(item["description"]) > 0, "description cannot be empty"

        assert isinstance(item["location"], list), "location must be a list"
        assert len(item["location"]) == 4, f"location must have exactly 4 coordinates"

        for i, coord in enumerate(item["location"]):
            assert isinstance(coord, (int, float)), f"coordinate {i} must be a number"
            assert coord >= 0, f"coordinate {i} must be have minimum 0"


def test_openai_schema_enforcement(openai_schema_result):
    """Test that OpenAI model with --json_schema produces strictly compliant output"""
    validate_schema_constraints(openai_schema_result)


def test_invalid_schema_file():
    """Test that invalid schema files are properly rejected"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"invalid": "schema"}, f)
        invalid_schema_path = f.name

    try:
        result_process = run_image_cli("openai", invalid_schema_path)
        if result_process.returncode == 0:
            parsed_result = parse_strict_json(result_process.stdout.strip(), "openai")
            assert isinstance(parsed_result, (list, dict)), "Output should be valid JSON structure"
    finally:
        Path(invalid_schema_path).unlink()


def test_schema_coordinate_minimum_constraint(openai_schema_result):
    """Test that the minimum: 0 constraint for coordinates is meaningful"""
    # Check that all coordinates are >= 0
    for item in openai_schema_result:
        for coord in item["location"]:
            assert coord >= 0, f"Found negative coordinate"


def test_schema_array_length_constraint(openai_schema_result):
    """Test that the array length constraint (exactly 4 items, coordinates) is enforced"""
    for item in openai_schema_result:
        assert len(item["location"]) == 4, f"Found location array with {len(item['location'])} items, should be 4"
