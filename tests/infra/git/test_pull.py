import subprocess
from unittest.mock import patch
import pytest

from infra.git.exceptions import GitPullError
from infra.git.pull import run_pull

def test_run_pull_calls_subprocess():
    with patch("subprocess.run") as mock_run:
        run_pull("/repo/path")

        mock_run.assert_called_once_with(
            ["git", "pull", "--force", "--no-rebase", "--no-edit"],
            cwd="/repo/path",
            check=True
        )

def test_run_pull_propagates_error():
    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")):
        with pytest.raises(GitPullError):
            run_pull("/repo/path")
