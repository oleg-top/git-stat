from pathlib import Path
from typing import Protocol, Iterator

from domain.models.repo import RepositoryFilePath, Repository, RepositoryPath


class RepositoryFilter(Protocol):
    def match(self, file_path: RepositoryFilePath) -> bool:
        pass

    @property
    def cache_key(self) -> str:
        pass


class ExtensionsFilter:
    def __init__(self, extensions: set[str]) -> None:
        self.__extensions = extensions

    def match(self, file_path: RepositoryFilePath) -> bool:
        ext = Path(file_path).suffix

        if ext not in self.__extensions:
            return False

        return True

    @property
    def cache_key(self) -> str:
        return f"ext:{','.join(self.__extensions)}"


class ExclusionsFilter:
    def __init__(self, exclusions: list[str]) -> None:
        self.__exclusions = exclusions

    def match(self, file_path: RepositoryFilePath) -> bool:
        path: Path = Path(file_path)
        to_exclude: bool = False

        for pattern in self.__exclusions:
            if path.match(pattern):
                to_exclude = True
                break

        if to_exclude:
            return False

        return True

    @property
    def cache_key(self) -> str:
        return f"exc:{','.join(self.__exclusions)}"


class RestrictionsFilter:
    def __init__(self, restrictions: list[str]) -> None:
        self.__restrictions = restrictions

    def match(self, file_path: RepositoryFilePath) -> bool:
        path: Path = Path(file_path)
        restrict: bool = True

        for pattern in self.__restrictions:
            if not path.match(pattern):
                restrict = False
                break

        if not restrict:
            return False

        return True

    @property
    def cache_key(self) -> str:
        return f"exc:{','.join(self.__restrictions)}"


class RepositoryFilterer(Protocol):
    def set(self, filters: list[RepositoryFilter]) -> None:
        pass

    def apply(self, repository: Repository) -> Repository:
        pass


class DefaultRepositoryFilterer:
    def __init__(self):
        self.__filters: list[RepositoryFilter] = []

    def set(self, filters: list[RepositoryFilter]) -> None:
        self.__filters = filters.copy()

    def apply(self, repository: Repository) -> Repository:
        class FilteredRepository:
            def __init__(
                    self,
                    repository_path: RepositoryPath,
                    filters: list[RepositoryFilter]
            ) -> None:
                self.__repository_path = repository_path
                self.__filters = filters

            def get_path(self) -> RepositoryPath:
                return self.__repository_path

            def __iter__(self) -> Iterator[RepositoryFilePath]:
                for path in repository:
                    to_yield = True
                    for f in self.__filters:
                        if not f.match(path):
                            to_yield = False

                    if to_yield:
                        yield path

        return FilteredRepository(
            repository_path=repository.get_path(),
            filters=self.__filters,
        )
