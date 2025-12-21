import hashlib
from pathlib import Path
from typing import Optional

from infra.git.clone import run_clone
from infra.git.git_repository import GitRepository


# TODO: имплементировать
class LocalGitRepositoryStorage:
    def __init__(self, storage_path: Optional[Path] = None) -> None:
        if storage_path is None:
            default_path = Path(__file__).resolve().parent / "data"
            default_path.mkdir(exist_ok=True)

            self.__storage_path: Path = default_path
        else:
            self.__storage_path: Path = storage_path

        self.__revision: str = "HEAD"
        self.__extensions: set[str] = set()
        self.__exclusions: list[str] = list()
        self.__restrictions: list[str] = list()

        self.__cloned_repositories: set[str] = set()

    def set_revision(self, revision: str) -> None:
        self.__revision = revision

    def set_extensions(self, extensions: set[str]) -> None:
        self.__extensions = extensions

    def set_exclusions(self, to_exclude: list[str]) -> None:
        self.__exclusions = to_exclude

    def set_restrictions(self, restrict_to: list[str]) -> None:
        self.__restrictions = restrict_to

    def __get_repository_path(self, repository_url: str) -> Path:
        url_bytes = repository_url.encode('utf-8')
        sha256_hash = hashlib.sha256(url_bytes).hexdigest()

        return self.__storage_path / sha256_hash

    def __is_repository_cloned(self, repository_url: str) -> bool:
        return self.__get_repository_path(repository_url).exists()

    def ensure(self, repository_url: str) -> GitRepository:
        if not self.__is_repository_cloned(repository_url):
            run_clone(
                repo_url=repository_url,
                path_to_store=str(self.__get_repository_path(repository_url)),
            )

        return GitRepository(
            repo_path=str(self.__get_repository_path(repository_url)),
            revision=self.__revision,
            extensions=self.__extensions,
            exclude=self.__exclusions,
            restrict_to=self.__restrictions,
        )

    def clean(self) -> None:
        pass
