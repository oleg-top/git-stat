import hashlib
from pathlib import Path
from typing import Optional

from infra.git.clone import run_clone
from infra.git.git_repository import GitRepository
from infra.git.pull import run_pull


class LocalGitRepositoryStorage:
    def __init__(self, storage_path: Optional[Path] = None) -> None:
        if storage_path is None:
            default_path = Path(__file__).resolve().parent / "data"
            default_path.mkdir(exist_ok=True)

            self.__storage_path: Path = default_path
        else:
            self.__storage_path: Path = storage_path

        self.__revision: str = "HEAD"
        self.__cloned_repositories: set[str] = set()

    def set_revision(self, revision: str) -> None:
        self.__revision = revision

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
        else:
            run_pull(repo_path=str(self.__get_repository_path(repository_url)))

        return GitRepository(
            repo_path=str(self.__get_repository_path(repository_url)),
            revision=self.__revision,
        )

    def clean(self) -> None:
        pass
