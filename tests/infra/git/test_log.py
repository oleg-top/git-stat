import io
import subprocess
from unittest.mock import patch, MagicMock
import pytest

from infra.git.exceptions import GitLogError
from infra.git.log import run_log

def test_run_log_returns_stringio():
    mock_result = MagicMock()
    mock_result.stdout = '"abc123 author@example.com John Doe"'

    with patch("infra.git.log.subprocess.run", return_value=mock_result) as mock_run:
        stream = run_log("/repo/path", "file.py", "HEAD")

        assert isinstance(stream, io.StringIO)
        assert stream.read() == 'abc123 author@example.com John Doe'

        mock_run.assert_called_once_with(
            ["git", "log", "HEAD", "--reverse", '--pretty=format:"%H %ae %an"', "--", "file.py", "|", "head", "-1"],
            cwd="/repo/path",
            capture_output=True,
            text=True,
            check=True,
        )

def test_run_log_propagates_subprocess_error():
    with patch("infra.git.log.subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")):
        with pytest.raises(GitLogError):
            run_log("/repo/path", "file.py", "HEAD")
