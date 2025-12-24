import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message
from adapters.telegram.handlers.start import cmd_start
from adapters.telegram.keyboards.main import get_main_keyboard

@pytest.mark.asyncio
async def test_cmd_start_clears_state_and_sends_message():
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    mock_state = AsyncMock()
    mock_state.clear = AsyncMock()

    await cmd_start(mock_message, mock_state)

    mock_state.clear.assert_awaited_once()

    mock_message.answer.assert_awaited_once()
    args, kwargs = mock_message.answer.await_args

    assert "Добро пожаловать в Git Statistics Bot" in args[0]
    assert kwargs["reply_markup"] == get_main_keyboard()
