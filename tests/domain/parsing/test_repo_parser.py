from unittest.mock import MagicMock

import pytest

from domain.models.stats import AuthorStats, AuthorData
from domain.parsing.repo_parser import RepoParser


@pytest.fixture
def repository():
    repo = MagicMock()
    repo.get_path.return_value = "/repo"

    repo.__iter__.return_value = iter([
        "file1.py",
        "file2.py",
    ])
    return repo


@pytest.fixture
def file_converter():
    converter = MagicMock()
    converter.stream.side_effect = lambda repository_path, file_path: f"stream:{file_path}"
    return converter


@pytest.fixture
def stream_parser():
    parser = MagicMock()

    parser.get_stream_stats.side_effect = [
        {
            "biba": AuthorStats(Author=AuthorData("biba", "email"), Lines=10, Files=1, Commits={"a1"}),
        },
        {
            "biba": AuthorStats(Author=AuthorData("biba", "email"), Lines=5, Files=1, Commits={"a2"}),
            "boba": AuthorStats(Author=AuthorData("boba", "email"), Lines=7, Files=1, Commits={"b1"}),
        },
    ]

    return parser


def test_calculate_stats_aggregates_by_author(
    repository,
    file_converter,
    stream_parser,
):
    parser = RepoParser(
        repository=repository,
        file_converter=file_converter,
        stream_parser=stream_parser,
    )

    stats = parser.calculate_stats()

    assert set(stats.keys()) == {"biba", "boba"}

    biba = stats["biba"]
    boba = stats["boba"]

    assert biba.Lines == 15
    assert biba.Files == 2
    assert biba.Commits == {"a1", "a2"}

    assert boba.Lines == 7
    assert boba.Files == 1
    assert boba.Commits == {"b1"}


def test_empty_repository_returns_empty_stats():
    repository = MagicMock()
    repository.get_path.return_value = "/repo"
    repository.__iter__.return_value = iter([])

    parser = RepoParser(
        repository=repository,
        file_converter=MagicMock(),
        stream_parser=MagicMock(),
    )

    stats = parser.calculate_stats()

    assert stats == {}
