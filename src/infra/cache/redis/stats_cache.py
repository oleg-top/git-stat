import pickle
from typing import Optional

from domain.models.stats import RepoStats
from infra.cache.redis.client import RedisClient


class RedisStatsCache:
    def __init__(
            self,
            redit_client: RedisClient,
            ttl_seconds: int,
    ) -> None:
        self.__redis = redit_client.client
        self.__ttl = ttl_seconds

    def get(self, key: str) -> Optional[RepoStats]:
        raw = self.__redis.get(key)
        if raw is None:
            return None

        return pickle.loads(raw)

    def set(self, key: str, repository_stats: RepoStats) -> None:
        data = pickle.dumps(repository_stats)
        self.__redis.setex(key, self.__ttl, data)
