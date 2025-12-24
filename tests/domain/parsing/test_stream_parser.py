import pytest
from unittest.mock import MagicMock

from domain.models.stats import AuthorStats
from domain.models.blame import (
    BlameCommitAuthorData, BlameFileAuthorData, BlameHashLine
)
from domain.parsing.stream_parser import StreamFileParser

@pytest.fixture
def parser():
    return StreamFileParser()

def make_author(name="biba"):
    return MagicMock(Name=name)

def make_commit(hash="hash1", author_name="biba", commiter_name="biba", commit_message="sth"):
    author = make_author(author_name)
    commiter = make_author(commiter_name)

    return BlameCommitAuthorData(
        Hash=hash,
        Author=author,
        Commiter=commiter,
        CommitMessage=commit_message,
    )

def make_file_author(hash="hash1", author_name="boba"):
    author = make_author(author_name)
    return BlameFileAuthorData(Hash=hash, Author=author)

def make_line(hash="hash1", lines=10, original_line=1, final_line=10):
    return BlameHashLine(
        Hash=hash,
        LinesChanged=lines,
        OriginalLine=original_line,
        FinalLine=final_line
    )

def test_empty_stream(parser):
    result = parser.get_stream_stats([])
    assert result == {}

def test_single_commit(parser):
    commit = make_commit()
    line = make_line()
    result = parser.get_stream_stats([commit, line])
    assert "biba" in result
    assert result["biba"].Lines == 10
    assert len(result["biba"].Commits) == 1
    assert result["biba"].Files == 1

def test_multiple_authors(parser):
    commit1 = make_commit("hash1", "biba")
    commit2 = make_commit("hash2", "boba")
    line1 = make_line("hash1", 5)
    line2 = make_line("hash2", 8)
    result = parser.get_stream_stats([commit1, commit2, line1, line2])
    assert result["biba"].Lines == 5
    assert result["boba"].Lines == 8

def test_file_author_integration(parser):
    file_author = make_file_author("hash1", "biba")
    line = make_line("hash1", 7)
    result = parser.get_stream_stats([file_author, line])
    assert result["biba"].Lines == 7
    assert result["biba"].Files == 1
