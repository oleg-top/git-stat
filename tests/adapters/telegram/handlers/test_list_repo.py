import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, User

from adapters.telegram.handlers.list_repo import list_repos


@pytest.mark.asyncio
async def test_list_repos_empty():
    mock_user = MagicMock(spec=User)
    mock_user.id = 123

    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = mock_user
    mock_message.answer = AsyncMock()

    mock_user_repos = MagicMock()
    mock_user_repos.list.return_value = []

    await list_repos(mock_message, mock_user_repos)

    mock_user_repos.list.assert_called_once_with(123)
    mock_message.answer.assert_awaited_once_with("📭 Список репозиториев пуст")


@pytest.mark.asyncio
async def test_list_repos_with_repos():
    mock_user = MagicMock(spec=User)
    mock_user.id = 123

    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = mock_user
    mock_message.answer = AsyncMock()

    mock_user_repos = MagicMock()
    mock_user_repos.list.return_value = [
        "https://github.com/oleg-top/git-stat1.git",
        "https://github.com/oleg-top/git-stat2.git",
    ]

    await list_repos(mock_message, mock_user_repos)

    mock_user_repos.list.assert_called_once_with(123)

    mock_message.answer.assert_awaited_once_with(
        "📂 Ваши репозитории:\n\n"
        "1. https://github.com/oleg-top/git-stat1.git\n"
        "2. https://github.com/oleg-top/git-stat2.git\n"
    )
