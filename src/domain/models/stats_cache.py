from typing import Protocol, Optional

from domain.models.stats import RepoStats


class StatsCache(Protocol):
    def get(self, repo_path: str) -> Optional[RepoStats]:
        pass

    def set(self, repo_path: str, repository_stats: RepoStats) -> None:
        pass
