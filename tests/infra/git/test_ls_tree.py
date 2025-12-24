import io
import subprocess
from unittest.mock import patch, MagicMock
import pytest

from infra.git.exceptions import GitLSTreeError
from infra.git.ls_tree import run_ls_tree

def test_run_ls_tree_returns_stringio():
    mock_result = MagicMock()
    mock_result.stdout = "file1.py\nfile2.py\n"

    with patch("subprocess.run", return_value=mock_result) as mock_run:
        stream = run_ls_tree("/repo/path", "HEAD")

        assert isinstance(stream, io.StringIO)
        assert stream.read() == "file1.py\nfile2.py\n"

        mock_run.assert_called_once_with(
            ["git", "ls-tree", "-r", "HEAD", "--name-only"],
            cwd="/repo/path",
            capture_output=True,
            text=True,
            check=True,
        )

def test_run_ls_tree_propagates_calledprocesserror():
    with patch("infra.git.ls_tree.subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")):
        with pytest.raises(GitLSTreeError):
            run_ls_tree("/repo/path", "HEAD")
