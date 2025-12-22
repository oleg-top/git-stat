import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from aiogram.fsm.context import FSMContext


class TestIntegration:

    @pytest.mark.asyncio
    async def test_full_repo_flow(self):
        from services.redis_service import redis_client

        user_id = 5000
        repo_link = "https://github.com/integration/test.git"
        revision = "integration-branch"

        assert not redis_client.repo_exists(user_id, repo_link, revision)
        assert len(redis_client.get_repos(user_id)) == 0

        result = redis_client.add_repo(user_id, repo_link, revision)
        assert result == 1

        assert redis_client.repo_exists(user_id, repo_link, revision)
        repos = redis_client.get_repos(user_id)
        assert len(repos) == 1
        assert repos[0]['link'] == repo_link
        assert repos[0]['revision'] == revision

        result_duplicate = redis_client.add_repo(user_id, repo_link, revision)
        assert result_duplicate == 0
        assert len(redis_client.get_repos(user_id)) == 1  # Все еще 1

        remove_result = redis_client.remove_repo(user_id, repo_link, revision)
        assert remove_result == 1

        assert not redis_client.repo_exists(user_id, repo_link, revision)
        assert len(redis_client.get_repos(user_id)) == 0

        remove_nonexistent = redis_client.remove_repo(user_id, repo_link, revision)
        assert remove_nonexistent == 0

    @pytest.mark.asyncio
    async def test_message_flow(self):
        from handlers.start import cmd_start
        from handlers.common import cmd_help, get_stats_info

        handlers_to_test = [
            (cmd_help, "Помощь по командам"),
            (get_stats_info, "Получение статистики"),
        ]

        for handler, expected_text in handlers_to_test:
            mock_message = AsyncMock()
            mock_message.answer = AsyncMock()

            await handler(mock_message)

            assert mock_message.answer.called
            assert expected_text in mock_message.answer.call_args[0][0]

        mock_message = AsyncMock()
        mock_message.answer = AsyncMock()
        mock_state = AsyncMock(spec=FSMContext)
        mock_state.clear = AsyncMock()

        await cmd_start(mock_message, mock_state)

        assert mock_message.answer.called
        assert "Добро пожаловать" in mock_message.answer.call_args[0][0]
        assert mock_state.clear.called
