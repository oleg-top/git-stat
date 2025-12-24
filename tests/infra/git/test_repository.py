import pytest
from unittest.mock import patch
from infra.git.git_repository import GitRepository

def test_git_repository_iter_yields_files():
    mock_files = ["file1.py\n", "dir/file2.cpp\n"]

    with patch("infra.git.git_repository.run_ls_tree", return_value=mock_files):
        repo = GitRepository("/repo/path", "HEAD")
        files = list(repo)

        assert files == ["file1.py", "dir/file2.cpp"]

def test_git_repository_get_path_returns_repo_path():
    repo = GitRepository("/repo/path", "HEAD")

    assert repo.get_path() == "/repo/path"
