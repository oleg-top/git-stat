from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from adapters.telegram.keyboards.main import get_main_keyboard

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    keyboard = get_main_keyboard()
    await message.answer(
        "ℹ️ **Помощь по командам:**\n\n"
        "• /start - Показать главное меню\n"
        "• /help - Показать это сообщение\n"
        "• /cancel - Отменить текущее действие\n\n"
        "**Основные функции:**\n"
        "• 📊 Получить статистику\n"
        "• ➕ Добавить репозиторий\n"
        "• 📂 Мои репозитории\n"
        "• 🗑️ Удалить репозиторий",
        parse_mode='Markdown',
        reply_markup=keyboard
    )


@router.message(F.text)
async def handle_unknown_message(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        return

    menu_buttons = [
        "📊 Получить статистику",
        "➕ Добавить репозиторий",
        "📂 Мои репозитории",
        "🗑️ Удалить репозиторий"
    ]

    if message.text in menu_buttons:
        return

    keyboard = get_main_keyboard()
    await message.answer(
        "🤔 Я не понимаю эту команду\n\n"
        "Используйте кнопки меню или /start для начала работы",
        reply_markup=keyboard
    )
