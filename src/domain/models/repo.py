from typing import Protocol, Iterator, TypeAlias


RepositoryPath: TypeAlias = str
RepositoryFilePath: TypeAlias = str


class Repository(Protocol):
    def get_path(self) -> RepositoryPath:
        pass

    def __iter__(self) -> Iterator[RepositoryFilePath]:
        pass
