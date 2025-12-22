from typing import Iterator

from domain.models.repo import RepositoryPath, RepositoryFilePath
from infra.git.ls_tree import run_ls_tree


class GitRepository:
    def __init__(
            self,
            repo_path: str,
            revision: str,
    ) -> None:
        self.__repo_path = repo_path
        self.__revision = revision

    def get_path(self) -> RepositoryPath:
        return self.__repo_path

    def __iter__(self) -> Iterator[RepositoryFilePath]:
        files = run_ls_tree(
            repo_path=self.__repo_path,
            revision=self.__revision,
        )

        for file in files:
            yield file.strip()

