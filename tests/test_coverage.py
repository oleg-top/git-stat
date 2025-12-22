import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.fsm.context import FSMContext
from services.redis_service import redis_client


class TestAdditionalCoverage:

    @pytest.mark.asyncio
    async def test_add_repo_invalid_url(self):
        from handlers.add_repo import add_repo_receive_link
        from aiogram.fsm.context import FSMContext

        mock_message = AsyncMock()
        mock_message.text = "invalid-url"
        mock_message.answer = AsyncMock()
        mock_state = AsyncMock(spec=FSMContext)

        await add_repo_receive_link(mock_message, mock_state)

        assert mock_message.answer.called
        assert "Неверный формат ссылки" in mock_message.answer.call_args[0][0]
        assert not mock_state.update_data.called
        assert not mock_state.set_state.called

    @pytest.mark.asyncio
    async def test_add_repo_cancel_command(self):
        from handlers.add_repo import add_repo_receive_link

        mock_message = AsyncMock()
        mock_message.text = "/cancel"
        mock_message.answer = AsyncMock()
        mock_state = AsyncMock(spec=FSMContext)
        mock_state.clear = AsyncMock()

        await add_repo_receive_link(mock_message, mock_state)

        assert mock_message.answer.called
        assert mock_state.clear.called

    def test_utils_edge_cases(self):
        from utils import is_valid_git_url, format_repo_list

        assert not is_valid_git_url("")
        assert not is_valid_git_url("   ")

        assert not is_valid_git_url(None)
        assert not is_valid_git_url(123)
        assert not is_valid_git_url([])

        assert "Список репозиториев пуст" in format_repo_list(None)
        assert "Список репозиториев пуст" in format_repo_list([])
        assert "Список репозиториев пуст" in format_repo_list("not a list")

        repos = [None, "string", 123, {"link": "https://github.com/test/repo.git", "revision": "main"}]
        result = format_repo_list(repos)
        assert "Ревизия: main" in result

        repos = [
            {"link": "https://github.com/test/repo.git"},
            {"revision": "main"},
            {},
        ]
        result = format_repo_list(repos)
        assert "Ревизия: main" in result

    def test_redis_edge_cases(self):
        result = redis_client.get_repos(0)
        assert result == []

        result = redis_client.remove_repo(999, "", "")
        assert result == 0

        result = redis_client.repo_exists(999, "", "")
        assert result is False

    @pytest.mark.asyncio
    async def test_handle_unknown_with_fsm_state(self):
        from handlers.common import handle_unknown_message

        mock_message = AsyncMock()
        mock_message.text = "неизвестно"
        mock_message.answer = AsyncMock()
        mock_state = AsyncMock(spec=FSMContext)
        mock_state.get_state.return_value = "some_state"

        await handle_unknown_message(mock_message, mock_state)

        assert not mock_message.answer.called

    @pytest.mark.asyncio
    async def test_handle_unknown_menu_button(self):
        from handlers.common import handle_unknown_message

        for button in ["➕ Добавить репозиторий", "📂 Мои репозитории", "🗑️ Удалить репозиторий"]:
            mock_message = AsyncMock()
            mock_message.text = button
            mock_message.answer = AsyncMock()
            mock_state = AsyncMock(spec=FSMContext)
            mock_state.get_state.return_value = None

            await handle_unknown_message(mock_message, mock_state)

            assert not mock_message.answer.called
