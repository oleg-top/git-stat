from dataclasses import dataclass
from typing import TypeAlias

CommitHash: TypeAlias = str
AuthorName: TypeAlias = str
AuthorEmail: TypeAlias = str


@dataclass
class AuthorData:
    Name: AuthorName
    Email: AuthorEmail


@dataclass
class AuthorStats:
    Author: AuthorData
    Lines: int
    Commits: set[CommitHash]
    Files: int


StreamStats: TypeAlias = dict[AuthorName, AuthorStats]
RepoStats: TypeAlias = dict[AuthorName, AuthorStats]
