from unittest.mock import mock_open, patch

import pytest

from ai_feedback.__main__ import _load_content_with_fallback


class TestLoadContentWithFallback:
    """Test cases for _load_content_with_fallback function - the core logic we rely on."""

    def test_load_content_predefined_name_success(self):
        """Test loading content using a predefined name."""
        content = "Test prompt content"
        predefined_values = ["test_prompt", "another_prompt"]

        with patch("builtins.open", mock_open(read_data=content)):
            with patch("os.path.join") as mock_join:
                mock_join.return_value = "/fake/path/user/test_prompt.md"

                result = _load_content_with_fallback("test_prompt", predefined_values, "user", "prompt")

                assert result == content
                mock_join.assert_called_once()

    def test_load_content_custom_file_path_success(self):
        """Test loading content using a custom file path."""
        content = "Custom file content"
        predefined_values = ["predefined_prompt"]

        with patch("builtins.open", mock_open(read_data=content)):
            result = _load_content_with_fallback("/custom/path/file.md", predefined_values, "user", "prompt")

            assert result == content

    def test_load_content_predefined_name_not_found(self, capsys):
        """Test error when predefined file is not found."""
        predefined_values = ["test_prompt"]

        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(SystemExit) as exc_info:
                _load_content_with_fallback("test_prompt", predefined_values, "user", "prompt")

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Pre-defined prompt file 'test_prompt.md' not found in user subfolder." in captured.out

    def test_load_content_custom_file_path_not_found(self, capsys):
        """Test error when custom file is not found."""
        predefined_values = ["predefined_prompt"]

        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(SystemExit) as exc_info:
                _load_content_with_fallback("/nonexistent/file.md", predefined_values, "user", "prompt")

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Prompt file '/nonexistent/file.md' not found." in captured.out
