import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, User, CallbackQuery, InlineKeyboardMarkup

from adapters.telegram.handlers.remove_repo import remove_repo_start, remove_repo_callback, cancel_remove


@pytest.mark.asyncio
async def test_remove_repo_start_no_repos():
    mock_user = MagicMock(spec=User)
    mock_user.id = 1

    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = mock_user
    mock_message.answer = AsyncMock()

    mock_user_repos = MagicMock()
    mock_user_repos.list.return_value = []

    await remove_repo_start(mock_message, mock_user_repos)

    mock_user_repos.list.assert_called_once_with(1)
    mock_message.answer.assert_awaited_once_with("📭 У вас нет репозиториев для удаления")


@pytest.mark.asyncio
async def test_remove_repo_start_with_repos():
    mock_user = MagicMock(spec=User)
    mock_user.id = 1

    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = mock_user
    mock_message.answer = AsyncMock()

    mock_user_repos = MagicMock()
    mock_user_repos.list.return_value = [
        "https://github.com/oleg-top/git-stat1.git",
        "https://github.com/oleg-top/git-stat2.git",
    ]

    await remove_repo_start(mock_message, mock_user_repos)

    mock_user_repos.list.assert_called_once_with(1)

    assert mock_message.answer.await_count == 1

    args, kwargs = mock_message.answer.await_args[0], mock_message.answer.await_args[1]

    assert "🗑️ Выберите репозиторий для удаления" in args[0]
    assert isinstance(kwargs["reply_markup"], InlineKeyboardMarkup)

    buttons = kwargs["reply_markup"].inline_keyboard

    assert buttons[0][0].text.startswith("🗑️ git-stat1")
    assert buttons[1][0].text.startswith("🗑️ git-stat2")
    assert buttons[2][0].text == "❌ Отменить"


@pytest.mark.asyncio
async def test_remove_repo_callback_exists():
    mock_user = MagicMock(spec=User)
    mock_user.id = 1

    mock_message = AsyncMock()
    mock_message.edit_text = AsyncMock()

    mock_callback = AsyncMock(spec=CallbackQuery)
    mock_callback.from_user = mock_user
    mock_callback.data = "remove:https://github.com/oleg-top/git-stat1.git"
    mock_callback.message = mock_message
    mock_callback.answer = AsyncMock()

    mock_user_repos = MagicMock()
    mock_user_repos.exists.return_value = True

    await remove_repo_callback(mock_callback, mock_user_repos)

    mock_user_repos.exists.assert_called_once_with(1, "https://github.com/oleg-top/git-stat1.git")
    mock_user_repos.remove.assert_called_once_with(1, "https://github.com/oleg-top/git-stat1.git")
    mock_message.edit_text.assert_awaited_once()
    mock_callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_remove_repo_callback_not_exists():
    mock_user = MagicMock(spec=User)
    mock_user.id = 1

    mock_message = AsyncMock()
    mock_message.edit_text = AsyncMock()

    mock_callback = AsyncMock(spec=CallbackQuery)
    mock_callback.from_user = mock_user
    mock_callback.data = "remove:https://github.com/oleg-top/git-stat1.git"
    mock_callback.message = mock_message
    mock_callback.answer = AsyncMock()

    mock_user_repos = MagicMock()
    mock_user_repos.exists.return_value = False

    await remove_repo_callback(mock_callback, mock_user_repos)

    mock_message.edit_text.assert_awaited_once_with("❌ Ошибка: репозиторий не найден")
    mock_callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_cancel_remove():
    mock_message = AsyncMock()
    mock_message.edit_text = AsyncMock()

    mock_callback = AsyncMock(spec=CallbackQuery)
    mock_callback.message = mock_message
    mock_callback.answer = AsyncMock()

    await cancel_remove(mock_callback)

    mock_message.edit_text.assert_awaited_once_with("❌ Удаление отменено")
    mock_callback.answer.assert_awaited_once()
