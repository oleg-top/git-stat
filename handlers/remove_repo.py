from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from services.redis_service import redis_client

router = Router()


@router.message(F.text == "🗑️ Удалить репозиторий")
async def remove_repo_start(message: types.Message):
    user_id = message.from_user.id
    repos = redis_client.get_repos(user_id)

    if not repos:
        await message.answer("📭 У вас нет репозиториев для удаления")
        return

    keyboard = []
    for repo_data in repos:
        repo_link = repo_data.get('link', '')
        revision = repo_data.get('revision', 'main')

        repo_name = repo_link.split('/')[-1]
        button_text = f"{repo_name} ({revision})"
        if len(button_text) > 30:
            button_text = button_text[:27] + "..."

        keyboard.append([
            InlineKeyboardButton(
                text=f"🗑️ {button_text}",
                callback_data=f"remove:{repo_link}:{revision}"
            )
        ])

    keyboard.append([InlineKeyboardButton("❌ Отменить", callback_data="cancel_remove")])

    await message.answer(
        "🗑️ Выберите репозиторий для удаления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@router.callback_query(F.data.startswith("remove:"))
async def remove_repo_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data.replace("remove:", "")

    parts = data.split(":", 1)
    if len(parts) != 2:
        await callback.answer("❌ Ошибка в данных")
        return

    repo_link, revision = parts

    result = redis_client.remove_repo(user_id, repo_link, revision)

    if result == 1:
        await callback.message.edit_text(
            f"✅ Репозиторий удален:\n\n"
            f"• Ссылка: `{repo_link}`\n"
            f"• Ревизия: `{revision}`",
            parse_mode='Markdown'
        )
    else:
        await callback.message.edit_text("❌ Ошибка: репозиторий не найден")

    await callback.answer()


@router.callback_query(F.data == "cancel_remove")
async def cancel_remove(callback: CallbackQuery):
    await callback.message.edit_text("❌ Удаление отменено")
    await callback.answer()
