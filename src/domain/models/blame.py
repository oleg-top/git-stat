from dataclasses import dataclass
from typing import Protocol, Iterator, TextIO, TypeAlias, Optional

from domain.models.repo import RepositoryFilePath
from domain.models.stats import AuthorData, AuthorName


class BlameEntry:
    pass


CommitHash: TypeAlias = str


@dataclass(frozen=True)
class BlameHashLine(BlameEntry):
    Hash: CommitHash
    OriginalLine: int
    FinalLine: int
    LinesChanged: int


@dataclass(frozen=True)
class BlameCommitAuthorData(BlameEntry):
    Author: AuthorData
    Commiter: AuthorData
    CommitMessage: str
    Hash: CommitHash


@dataclass(frozen=True)
class BlameFileAuthorData(BlameEntry):
    Author: AuthorData
    Hash: CommitHash


BlameStream: TypeAlias = Iterator[BlameEntry]

