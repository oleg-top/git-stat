import pytest
from unittest.mock import patch
from infra.git.git_repository import GitRepository
from infra.storage.local.storage import LocalGitRepositoryStorage


@pytest.fixture
def storage(tmp_path):
    return LocalGitRepositoryStorage(storage_path=tmp_path)


@patch("infra.storage.local.storage.run_pull")
@patch("infra.storage.local.storage.run_clone")
def test_ensure_calls_clone_for_new_repo(mock_clone, mock_pull, storage):
    repo_url = "https://github.com/oleg-top/git-stat.git"
    repo_path = storage._LocalGitRepositoryStorage__get_repository_path(repo_url)
    print(repo_path)

    assert not repo_path.exists()

    result = storage.ensure(repo_url)

    mock_clone.assert_called_once_with(repo_url=repo_url, path_to_store=str(repo_path))
    mock_pull.assert_not_called()

    assert isinstance(result, GitRepository)


@patch("infra.storage.local.storage.run_pull")
@patch("infra.storage.local.storage.run_clone")
def test_ensure_calls_pull_for_existing_repo(mock_clone, mock_pull, storage):
    repo_url = "https://github.com/oleg-top/git-stat.git"
    repo_path = storage._LocalGitRepositoryStorage__get_repository_path(repo_url)

    repo_path.mkdir(parents=True, exist_ok=True)

    result = storage.ensure(repo_url)

    mock_pull.assert_called_once_with(repo_path=str(repo_path))
    mock_clone.assert_not_called()

    assert isinstance(result, GitRepository)
