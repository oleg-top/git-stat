from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main import get_main_keyboard
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()

    keyboard = get_main_keyboard()
    await message.answer(
        "🤖 Добро пожаловать в Git Statistics Bot!\n\n"
        "Я помогу вам анализировать статистику Git репозиториев.\n"
        "Выберите действие:",
        reply_markup=keyboard
    )
