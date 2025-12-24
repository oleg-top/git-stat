import io
from unittest.mock import patch, MagicMock
import pytest

from infra.git.exceptions import GitBlameError, GitLogError
from infra.git.file_converter import GitFileConverter
from domain.models.blame import BlameFileAuthorData, BlameCommitAuthorData, BlameHashLine, AuthorData


@pytest.fixture
def converter():
    return GitFileConverter(revision="HEAD")


def make_blame_lines():
    lines = (
'''
c676b9019f7815dfcb14db593e52492ff2b646d4 183 183 1
author Aleksandr Komarov
author-mail <alevalkomarov@edu.hse.ru>
author-time 1766435463
author-tz +0300
committer Aleksandr Komarov
committer-mail <alevalkomarov@edu.hse.ru>
committer-time 1766435463
committer-tz +0300
summary poshla zhara
'''
    )
    return io.StringIO(lines)


@patch("infra.git.file_converter.run_blame")
@patch("infra.git.file_converter.run_log")
def test_stream_file_empty(run_log_mock, run_blame_mock, converter):
    run_blame_mock.return_value = io.StringIO("")
    run_log_mock.return_value = io.StringIO("f5846893cb99408d878d538b863752e13361d4fd alevalkomarov@edu.hse.ru Aleksandr Komarov")

    result = list(converter.stream("/repo", "file.py"))

    assert any(isinstance(r, BlameFileAuthorData) for r in result)

    run_blame_mock.assert_called_once()
    run_log_mock.assert_called_once()


@patch("infra.git.file_converter.run_blame")
def test_stream_normal_file(run_blame_mock, converter):
    run_blame_mock.return_value = make_blame_lines()

    result = list(converter.stream("/repo", "file.py"))

    assert any(isinstance(r, BlameCommitAuthorData) or isinstance(r, BlameHashLine) for r in result)

    run_blame_mock.assert_called_once()


@patch("infra.git.file_converter.run_blame")
def test_stream_blame_raises_exception(run_blame_mock, converter):
    run_blame_mock.side_effect = GitBlameError("git error")

    with pytest.raises(GitBlameError):
        list(converter.stream("/repo", "file.py"))


@patch("infra.git.file_converter.run_blame")
@patch("infra.git.file_converter.run_log")
def test_stream_log_raises_exception(run_log_mock, run_blame_mock, converter):
    run_blame_mock.return_value = io.StringIO("")
    run_log_mock.side_effect = GitLogError("log error")

    with pytest.raises(GitLogError):
        list(converter.stream("/repo", "file.py"))
