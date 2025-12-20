from typing import Protocol, Iterator, TypeAlias

from domain.models.blame import BlameStream


RepoPath: TypeAlias = str


class Repository(Protocol):
    def get_path(self) -> RepoPath:
        pass

    def __iter__(self) -> Iterator[BlameStream]:
        pass
