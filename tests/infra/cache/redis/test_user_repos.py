from unittest.mock import MagicMock
import pytest
from infra.cache.redis.client import RedisClient
from infra.cache.redis.user_repos import RedisUserRepositories

def make_mock_redis():
    mock_redis = MagicMock()
    client = RedisUserRepositories(redis_client=MagicMock(client=mock_redis))
    return client, mock_redis

def test_add_calls_sadd():
    repos, mock_redis = make_mock_redis()
    repos.add(123, "https://github.com/oleg-top/git-stat.git")
    mock_redis.sadd.assert_called_once_with("user:123:repos", "https://github.com/oleg-top/git-stat.git")

def test_list_returns_decoded_strings():
    repos, mock_redis = make_mock_redis()
    mock_redis.smembers.return_value = [b"https://github.com/oleg-top/git-stat1.git", b"https://github.com/oleg-top/git-stat2.git"]
    result = repos.list(123)
    assert result == ["https://github.com/oleg-top/git-stat1.git", "https://github.com/oleg-top/git-stat2.git"]
    mock_redis.smembers.assert_called_once_with("user:123:repos")

def test_exists_returns_true_or_false():
    repos, mock_redis = make_mock_redis()
    mock_redis.sismember.return_value = True
    assert repos.exists(123, "url") is True
    mock_redis.sismember.return_value = False
    assert repos.exists(123, "url") is False

def test_remove_calls_srem():
    repos, mock_redis = make_mock_redis()
    repos.remove(123, "https://github.com/oleg-top/git-stat.git")
    mock_redis.srem.assert_called_once_with("user:123:repos", "https://github.com/oleg-top/git-stat.git")
