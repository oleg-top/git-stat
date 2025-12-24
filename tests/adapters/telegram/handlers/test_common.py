import pytest
from unittest.mock import AsyncMock
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from adapters.telegram.handlers.common import cmd_help, handle_unknown_message


@pytest.mark.asyncio
async def test_cmd_help_sends_message():
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    await cmd_help(mock_message)

    mock_message.answer.assert_awaited_once()
    args, kwargs = mock_message.answer.call_args

    assert "ℹ️ **Помощь по командам:**" in args[0]
    assert "reply_markup" in kwargs


@pytest.mark.asyncio
async def test_handle_unknown_message_unknown_text_replies_with_keyboard():
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "bebebe"
    mock_message.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_state = AsyncMock(return_value=None)

    await handle_unknown_message(mock_message, mock_state)

    mock_message.answer.assert_awaited_once()
    args, kwargs = mock_message.answer.call_args
    assert "🤔 Я не понимаю эту команду" in args[0]
    assert "reply_markup" in kwargs
