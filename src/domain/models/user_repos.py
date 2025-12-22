from typing import Protocol


class UserRepositories(Protocol):
    def add(self, user_id: int, repo_url: str) -> None:
        pass

    def list(self, user_id: int) -> list[str]:
        pass

    def exists(self, user_id: int, repo_url: str) -> bool:
        pass
