import redis


class RedisClient:
    def __init__(
            self,
            host: str,
            port: int,
    ) -> None:
        self.__client = redis.Redis(
            host=host,
            port=port
        )

    @property
    def client(self) -> redis.Redis:
        return self.__client

