from pathlib import Path

from tests.test_helper import run_cli_and_capture, mock_and_capture


def test_ggr274_question1_deepseek_markdown(capsys, mock_and_capture):
    """
    Example 4:
    Evaluate question 1 of test1 of ggr274 homework using DeepSeek model, output as Markdown.
    python -m ai_feedback --prompt code_table --scope code \
        --submission test_submissions/ggr274_homework5/test1/student_submission.ipynb \
        --question 1 --model deepSeek-R1:70B --output markdown
    """
    parent = Path(__file__).parent.parent.parent

    args = [
        "--prompt", "code_table",
        "--scope", "code",
        "--submission", str(parent / "test_submissions/ggr274_homework5/test1/student_submission.ipynb"),
        "--question", "1",
        "--model", "deepSeek-R1:70B",
        "--output", "markdown",
    ]
    output = run_cli_and_capture(args, capsys)
    assert "Markdown report saved" in output
