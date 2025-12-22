import hashlib
import json
from dataclasses import dataclass
from typing import Protocol, Optional

from domain.models.stats import RepoStats

@dataclass(frozen=True)
class RepositoryStatsCacheKey:
    repository_url: str
    revision: str
    filters: tuple[str, ...]


def make_stats_cache_key(key: RepositoryStatsCacheKey) -> str:
    data = {
        "repository": key.repository_url,
        "revision": key.revision,
        "filters": key.filters,
    }

    raw = json.dumps(data, sort_keys=True, separators=(",", ":"))

    return f"repository-stats:{hashlib.sha256(raw.encode()).hexdigest()}"


class StatsCache(Protocol):
    def get(self, key: str) -> Optional[RepoStats]:
        pass

    def set(self, key: str, stats: RepoStats) -> None:
        pass


