from typing import Protocol

from domain.models.blame import BlameStream
from domain.models.repo import RepositoryFilePath, RepositoryPath


class FileConverter(Protocol):
    def stream(
            self,
            repository_path: RepositoryPath,
            file_path: RepositoryFilePath
    ) -> BlameStream:
        pass
