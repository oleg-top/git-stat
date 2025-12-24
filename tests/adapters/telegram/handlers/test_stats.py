import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message

from adapters.telegram.handlers.stats import stats_start, StatsStates, stats_receive_repo, stats_receive_filters
from domain.models.user_repos import UserRepositories
from app.use_cases.dummy_parse_repository import ParseRepositoryUseCase


@pytest.mark.asyncio
async def test_stats_start_sets_state():
    mock_user = MagicMock()
    mock_user.id = 1

    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = mock_user
    mock_message.answer = AsyncMock()
    mock_state = AsyncMock()
    mock_user_repos = AsyncMock(spec=UserRepositories)
    mock_user_repos.list.return_value = ["repo1", "repo2"]

    await stats_start(mock_message, mock_state, mock_user_repos)

    mock_message.answer.assert_awaited_once()
    mock_state.set_state.assert_awaited_once_with(StatsStates.waiting_for_repo)


@pytest.mark.asyncio
async def test_stats_receive_repo_cancel():
    mock_user = MagicMock()
    mock_user.id = 1

    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = mock_user
    mock_message.text = "/cancel"
    mock_message.answer = AsyncMock()
    mock_state = AsyncMock()
    mock_user_repos = AsyncMock(spec=UserRepositories)

    await stats_receive_repo(mock_message, mock_state, mock_user_repos)

    mock_state.clear.assert_awaited_once()
    mock_message.answer.assert_awaited()


@pytest.mark.asyncio
async def test_stats_receive_filters_main_flow():
    mock_user = MagicMock()
    mock_user.id = 1

    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = mock_user
    mock_message.text = "ext:.py;exc:tests/*;res:src/*.py"
    mock_message.answer = AsyncMock()

    mock_state = AsyncMock()
    mock_state.get_data.return_value = {
        "repo_link": "https://github.com/oleg-top/git-stat.git",
        "revision": "HEAD"
    }

    mock_parse_uc = MagicMock(spec=ParseRepositoryUseCase)
    mock_parse_uc.storage = MagicMock()
    mock_parse_uc.file_converter = MagicMock()
    mock_parse_uc.execute = MagicMock(return_value={
        "biba": MagicMock(Lines=10, Files=2),
        "boba": MagicMock(Lines=5, Files=1)
    })

    await stats_receive_filters(mock_message, mock_state, mock_parse_uc)

    mock_parse_uc.storage.set_revision.assert_called_once_with("HEAD")
    mock_parse_uc.file_converter.set_revision.assert_called_once_with("HEAD")
    mock_message.answer.assert_awaited()
    mock_state.clear.assert_awaited_once()
