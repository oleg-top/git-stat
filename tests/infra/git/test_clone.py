import subprocess
from unittest.mock import patch, MagicMock
import pytest

from infra.git.clone import run_clone
from infra.git.exceptions import GitCloneError


def test_run_clone_calls_subprocess_run(tmp_path):
    repo_url = "https://github.com/oleg-top/git-stat.git"
    path_to_store = tmp_path / "repo"

    mock_result = MagicMock()
    with patch("infra.git.clone.subprocess.run", return_value=mock_result) as mock_run:
        run_clone(repo_url, str(path_to_store))
        mock_run.assert_called_once_with(
            ["git", "clone", repo_url, str(path_to_store)],
            capture_output=True,
            text=True,
            check=True,
        )


def test_run_clone_propagates_calledprocesserror(tmp_path):
    repo_url = "https://github.com/oleg-top/git-stat.git"
    path_to_store = tmp_path / "repo"

    with patch(
        "infra.git.clone.subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "git clone")
    ):
        with pytest.raises(GitCloneError):
            run_clone(repo_url, str(path_to_store))
