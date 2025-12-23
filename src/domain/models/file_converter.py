from typing import Protocol

from domain.models.blame import BlameStream
from domain.models.repo import RepositoryFilePath, RepositoryPath


class FileConverter(Protocol):
    def set_revision(self, revision: str) -> None:
        pass

    def stream(
            self,
            repository_path: RepositoryPath,
            file_path: RepositoryFilePath
    ) -> BlameStream:
        pass
