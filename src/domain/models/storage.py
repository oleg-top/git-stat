from typing import Protocol

from domain.models.repo import Repository


class RepositoryStorage(Protocol):
    def set_revision(self, revision: str) -> None:
        pass

    def ensure(self, repo_url: str) -> Repository:
        pass

    def clean(self) -> None:
        pass
