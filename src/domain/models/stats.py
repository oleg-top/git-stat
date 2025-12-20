from dataclasses import dataclass
from typing import TypeAlias

from domain.models.blame import CommitHash

AuthorName: TypeAlias = str
AuthorEmail: TypeAlias = str


@dataclass(frozen=True)
class AuthorData:
    Name: AuthorName
    Email: AuthorEmail


@dataclass(frozen=True)
class AuthorStats:
    Author: AuthorData
    Lines: int
    Commits: set[CommitHash]
    Files: int


StreamStats: TypeAlias = dict[AuthorName, AuthorStats]
RepoStats: TypeAlias = dict[AuthorName, AuthorStats]
