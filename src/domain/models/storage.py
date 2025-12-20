from typing import Protocol, Optional

from domain.models.repo import Repository


class RepositoryStorage(Protocol):
    def get(self, repo_url: str) -> Optional[Repository]:  # signature may change in future
        pass

    def set(self, repository: Repository) -> None:
        pass

    def clean(self) -> None:
        pass
