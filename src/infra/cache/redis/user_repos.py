from infra.cache.redis.client import RedisClient


class RedisUserRepositories:
    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client.client

    @staticmethod
    def __get_key(user_id: int) -> str:
        return f"user:{user_id}:repos"

    def add(self, user_id: int, repo_url: str) -> None:
        self.redis.sadd(self.__get_key(user_id), repo_url)

    def list(self, user_id: int) -> list[str]:
        repos = self.redis.smembers(self.__get_key(user_id))
        return [r.decode("utf-8") for r in repos]

    def exists(self, user_id: int, repo_url: str) -> bool:
        return bool(self.redis.sismember(self.__get_key(user_id), repo_url))

    def remove(self, user_id: int, repo_url: str) -> None:
        self.redis.srem(self.__get_key(user_id), repo_url)
