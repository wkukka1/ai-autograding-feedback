from pathlib import Path

from tests.test_helper import mock_and_capture, run_cli_and_capture


def test_cnn_example_openai_stdout(capsys, mock_and_capture):
    """Example 1:
    Evaluate cnn_example test using openAI model and print to stdout.
    python -m ai_feedback --prompt code_lines --scope code \
        --submission test_submissions/cnn_example/cnn_submission \
        --solution test_submissions/cnn_example/cnn_solution.py \
        --model openai --output stdout
    """
    parent = Path(__file__).parent.parent.parent

    args = [
        "--prompt",
        "code_lines",
        "--scope",
        "code",
        "--submission",
        str(parent / "test_submissions/cnn_example/cnn_submission.py"),
        "--solution",
        str(parent / "test_submissions/cnn_example/cnn_solution.py"),
        "--model",
        "openai",
    ]
    output = run_cli_and_capture(args, capsys)

    assert "Compare the student's code and solution code. For each mistake" in output
    assert "(Line 1) import numpy as np" in output
    assert '<submission filename="cnn_submission.py">' in output
    assert '<solution filename="cnn_solution.py">' in output


def test_cnn_example_custom_prompt_stdout(capsys, mock_and_capture):
    """Example 2:
    Evaluate cnn_example test using openAI model and a custom prompt text, printing to stdout.
    python -m ai_feedback --prompt_text "Evaluate the student's code readability." \
        --scope code \
        --submission test_submissions/cnn_example/cnn_submission.py \
        --model openai \
        --output stdout
    """
    parent = Path(__file__).parent.parent.parent

    args = [
        "--prompt_text",
        "Evaluate the student's code readability.\n {file_contents}",
        "--scope",
        "code",
        "--submission",
        str(parent / "test_submissions/cnn_example/cnn_submission.py"),
        "--model",
        "openai",
    ]
    output = run_cli_and_capture(args, capsys)
    assert "Evaluate the student's code readability." in output
    assert '<submission filename="cnn_submission.py">' in output
    assert "(Line 1) import numpy as np" in output


def test_pdf_example_openai_direct(capsys, mock_and_capture):
    """Example 3:
    Evaluate pdf_example test using openAI model and direct output mode.
    python -m ai_feedback --prompt text_pdf_analyze --scope text \
        --submission test_submissions/pdf_example/student_pdf_submission.pdf \
        --model openai --output direct
    """
    parent = Path(__file__).parent.parent.parent
    args = [
        "--prompt",
        "text_pdf_analyze",
        "--scope",
        "text",
        "--submission",
        str(parent / "test_submissions/pdf_example/student_pdf_submission.pdf"),
        "--model",
        "openai",
    ]

    output = run_cli_and_capture(args, capsys)
    assert "Does the student correctly respond to the question, and meet all the" in output
    assert "student_pdf_submission.pdf" in output
    assert "Normalization allows each feature to have an equal influence on the mode" in output


def test_xml_formatting_code_scope(capsys, mock_and_capture):
    """
    Test XML formatting for file contents in code scope.
    Verifies that file contents use XML tags while file references remain plain text.
    """
    parent = Path(__file__).parent.parent.parent

    args = [
        "--prompt_text",
        "File references: {file_references}\n\nFile contents:\n{file_contents}",
        "--scope",
        "code",
        "--submission",
        str(parent / "test_submissions/csc108/correct_submission/correct_submission.py"),
        "--solution",
        str(parent / "test_submissions/csc108/solution.py"),
        "--model",
        "openai",
    ]
    output = run_cli_and_capture(args, capsys)

    assert "The student's submission file is correct_submission.py." in output
    assert "The instructor's solution file is solution.py." in output

    assert '<submission filename="correct_submission.py">' in output
    assert '</submission>' in output
    assert '<solution filename="solution.py">' in output
    assert '</solution>' in output

    assert "(Line 1) def fizzbuzz(n: int) -> list:" in output


def test_xml_formatting_text_scope_with_test_output(capsys, mock_and_capture):
    """
    Test XML formatting for file contents in text scope with all file types.
    Verifies submission, solution, and test_output files all use XML formatting.
    """
    parent = Path(__file__).parent.parent.parent

    args = [
        "--prompt_text",
        "File references: {file_references}\n\nFile contents:\n{file_contents}",
        "--submission_type",
        "python",
        "--scope",
        "text",
        "--submission",
        str(parent / "test_submissions/ggr274_homework5/test1/student_submission.txt"),
        "--solution",
        str(parent / "test_submissions/ggr274_homework5/test1/Homework_5_solution.txt"),
        "--model",
        "openai",
    ]
    output = run_cli_and_capture(args, capsys)

    assert "The student's submission file is student_submission.txt." in output
    assert "The instructor's solution file is Homework_5_solution.txt." in output

    assert '<submission filename="student_submission.txt">' in output
    assert '</submission>' in output
    assert '<solution filename="Homework_5_solution.txt">' in output
    assert '</solution>' in output
