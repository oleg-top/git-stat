from typing import Protocol

from domain.models.storage import RepositoryStorage
from domain.parsing.stream_parser import StreamParser


class UseCase(Protocol):
    def __init__(
            self,
            storage: RepositoryStorage,
            stream_parser: StreamParser,
    ) -> None:
        pass

    def execute(self) -> None:
        pass