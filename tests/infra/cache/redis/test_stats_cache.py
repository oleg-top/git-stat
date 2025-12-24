import pickle
from unittest.mock import MagicMock
import pytest
from infra.cache.redis.client import RedisClient
from infra.cache.redis.stats_cache import RedisStatsCache


def test_get_returns_none_when_key_missing():
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    cache = RedisStatsCache(redit_client=MagicMock(client=mock_redis), ttl_seconds=60)

    result = cache.get("missing_key")
    assert result is None
    mock_redis.get.assert_called_once_with("missing_key")


def test_get_returns_deserialized_data():
    mock_redis = MagicMock()
    sample_data = {"author": {"Lines": 10, "Files": 2}}
    mock_redis.get.return_value = pickle.dumps(sample_data)
    cache = RedisStatsCache(redit_client=MagicMock(client=mock_redis), ttl_seconds=60)

    result = cache.get("key")
    assert result == sample_data
    mock_redis.get.assert_called_once_with("key")


def test_set_calls_setex_with_pickled_data():
    mock_redis = MagicMock()
    cache = RedisStatsCache(redit_client=MagicMock(client=mock_redis), ttl_seconds=60)
    sample_data = {"author": {"Lines": 10, "Files": 2}}

    cache.set("key", sample_data)

    args, kwargs = mock_redis.setex.call_args
    assert args[0] == "key"
    assert args[1] == 60
    assert pickle.loads(args[2]) == sample_data
