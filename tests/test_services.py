import pytest
from services.redis_service import RedisService


class TestRedisServiceClass:

    def test_init(self):
        service = RedisService()
        assert service._data == {}

    def test_multiple_users(self):
        service = RedisService()

        service.add_repo(1, "https://github.com/user1/repo.git", "main")
        assert len(service.get_repos(1)) == 1

        service.add_repo(2, "https://github.com/user2/repo.git", "master")
        assert len(service.get_repos(2)) == 1

        assert len(service.get_repos(1)) == 1
        assert len(service.get_repos(2)) == 1

    def test_repo_exists(self):
        service = RedisService()

        service.add_repo(100, "https://github.com/test/exists.git", "main")

        assert service.repo_exists(100, "https://github.com/test/exists.git", "main")
        assert not service.repo_exists(100, "https://github.com/test/notexists.git", "main")
        assert not service.repo_exists(999, "https://github.com/test/exists.git", "main")  # Другой пользователь

    def test_clear_data(self):
        service = RedisService()

        service.add_repo(1, "https://github.com/test/repo.git", "main")
        assert len(service.get_repos(1)) == 1

        service._data.clear()
        assert len(service.get_repos(1)) == 0
