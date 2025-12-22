import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, CallbackQuery, User, Chat
from aiogram.fsm.context import FSMContext
from services.redis_service import redis_client


class TestHandlers:

    @pytest.mark.asyncio
    async def test_start_handler(self):
        from handlers.start import cmd_start

        mock_message = AsyncMock(spec=Message)
        mock_message.answer = AsyncMock()
        mock_state = AsyncMock(spec=FSMContext)
        mock_state.clear = AsyncMock()

        await cmd_start(mock_message, mock_state)

        assert mock_message.answer.called
        assert "Добро пожаловать" in mock_message.answer.call_args[0][0]
        assert mock_state.clear.called

    @pytest.mark.asyncio
    async def test_help_handler(self):
        from handlers.common import cmd_help

        mock_message = AsyncMock(spec=Message)
        mock_message.answer = AsyncMock()

        await cmd_help(mock_message)

        assert mock_message.answer.called
        assert "Помощь по командам" in mock_message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_get_stats_info(self):
        from handlers.common import get_stats_info

        mock_message = AsyncMock(spec=Message)
        mock_message.answer = AsyncMock()

        await get_stats_info(mock_message)

        assert mock_message.answer.called
        assert "Получение статистики" in mock_message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_list_repos_empty(self):
        from handlers.list_repo import list_repos

        mock_user = MagicMock(spec=User)
        mock_user.id = 111

        mock_message = AsyncMock(spec=Message)
        mock_message.from_user = mock_user
        mock_message.answer = AsyncMock()

        await list_repos(mock_message)

        assert mock_message.answer.called
        response = mock_message.answer.call_args[0][0]
        assert any(text in response for text in ["Список репозиториев пуст", "У вас еще нет"])
