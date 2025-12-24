import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message

from adapters.telegram.handlers.add_repo import add_repo_start, AddRepoStates, add_repo_receive_link, cancel_any_state


@pytest.mark.asyncio
async def test_add_repo_start_sets_state():
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()
    mock_state = AsyncMock()

    await add_repo_start(mock_message, mock_state)

    mock_message.answer.assert_awaited_once()
    mock_state.set_state.assert_awaited_once_with(AddRepoStates.waiting_for_link)


@pytest.mark.asyncio
async def test_add_repo_receive_link_cancel():
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/cancel"

    mock_message.from_user = MagicMock()
    mock_message.from_user.id = 1

    mock_message.answer = AsyncMock()
    mock_state = AsyncMock()
    mock_state.get_state = AsyncMock(return_value=AddRepoStates.waiting_for_link)
    mock_add_repo_uc = AsyncMock()

    await add_repo_receive_link(mock_message, mock_state, mock_add_repo_uc)

    mock_state.clear.assert_awaited_once()
    mock_message.answer.assert_awaited_with("❌ Добавление репозитория отменено")


@pytest.mark.asyncio
async def test_add_repo_receive_link_invalid_url():
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "invalid"

    mock_message.from_user = MagicMock()
    mock_message.from_user.id = 1

    mock_message.answer = AsyncMock()
    mock_state = AsyncMock()
    mock_add_repo_uc = AsyncMock()

    await add_repo_receive_link(mock_message, mock_state, mock_add_repo_uc)

    mock_message.answer.assert_awaited()
    mock_add_repo_uc.execute.assert_not_called()


@pytest.mark.asyncio
async def test_add_repo_receive_link_success():
    repo_url = "https://github.com/oleg-top/git-stat.git"

    mock_message = AsyncMock(spec=Message)
    mock_message.text = repo_url

    mock_message.from_user = MagicMock()
    mock_message.from_user.id = 1

    mock_message.answer = AsyncMock()
    mock_state = AsyncMock()
    mock_add_repo_uc = AsyncMock()
    mock_add_repo_uc.execute = AsyncMock(return_value=True)

    await add_repo_receive_link(mock_message, mock_state, mock_add_repo_uc)

    mock_add_repo_uc.execute.assert_called_once()
    mock_message.answer.assert_awaited()
    mock_state.clear.assert_awaited_once()


@pytest.mark.asyncio
async def test_cancel_any_state_no_state():
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()
    mock_state = AsyncMock()
    mock_state.get_state = AsyncMock(return_value=None)

    await cancel_any_state(mock_message, mock_state)

    mock_message.answer.assert_awaited_with("❌ Нет активных операций для отмены")


@pytest.mark.asyncio
async def test_cancel_any_state_with_state():
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()
    mock_state = AsyncMock()
    mock_state.get_state = AsyncMock(return_value="waiting_for_link")

    await cancel_any_state(mock_message, mock_state)

    mock_state.clear.assert_awaited_once()
    mock_message.answer.assert_awaited()
