from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="📊 Получить статистику")],
        [
            KeyboardButton(text="➕ Добавить репозиторий"),
            KeyboardButton(text="📂 Мои репозитории")
        ],
        [KeyboardButton(text="🗑️ Удалить репозиторий")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
