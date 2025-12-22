from dataclasses import dataclass
from typing import Protocol, Optional

from domain.models.stats import RepoStats

@dataclass(frozen=True)
class RepositoryStatsCacheKey:
    repository_url: str
    revision: str
    filters: tuple[str, ...]


class StatsCache(Protocol):
    def get(self, key: str) -> Optional[RepoStats]:
        pass

    def set(self, key: str, stats: RepoStats) -> None:
        pass
