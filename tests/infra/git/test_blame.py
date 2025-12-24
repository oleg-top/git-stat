import io
from unittest.mock import patch, MagicMock
import pytest
import subprocess

from infra.git.blame import run_blame
from infra.git.exceptions import GitBlameError


def test_run_blame_returns_stringio():
    mock_result = MagicMock()
    mock_result.stdout = "blame output"

    with patch("infra.git.blame.subprocess.run", return_value=mock_result) as mock_run:
        stream = run_blame("/repo/path", "file.py", "HEAD")

        assert isinstance(stream, io.StringIO)
        assert stream.read() == "blame output"

        mock_run.assert_called_once_with(
            ["git", "blame", "--incremental", "file.py", "HEAD"],
            cwd="/repo/path",
            capture_output=True,
            text=True,
            check=True,
        )


def test_run_blame_propagates_subprocess_error():
    with patch(
        "infra.git.blame.subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "cmd")
    ):
        with pytest.raises(GitBlameError):
            run_blame("/repo/path", "file.py", "HEAD")
