from typing import Protocol

from domain.models.file_converter import FileConverter
from domain.models.filterer import RepositoryFilterer, RepositoryFilter
from domain.models.stats import RepoStats
from domain.models.storage import RepositoryStorage
from domain.parsing.stream_parser import StreamParser


class UseCase(Protocol):
    def __init__(
            self,
            storage: RepositoryStorage,
            file_converter: FileConverter,
            filterer: RepositoryFilterer,
            stream_parser: StreamParser,
    ) -> None:
        pass

    def execute(self, repository_url: str, filters: list[RepositoryFilter]) -> RepoStats:
        pass
