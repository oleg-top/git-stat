from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from domain.models.user_repos import UserRepositories

router = Router()


@router.message(F.text == "🗑️ Удалить репозиторий")
async def remove_repo_start(
    message: types.Message,
    user_repos: UserRepositories,
):
    user_id = message.from_user.id
    repos = user_repos.list(user_id)

    if not repos:
        await message.answer("📭 У вас нет репозиториев для удаления")
        return

    keyboard = []
    for repo_link in repos:
        repo_name = repo_link.split('/')[-1]
        display_name = repo_name if len(repo_name) <= 30 else repo_name[:27] + "..."
        keyboard.append([
            InlineKeyboardButton(
                text=f"🗑️ {display_name}",
                callback_data=f"remove:{repo_link}"
            )
        ])

    keyboard.append([InlineKeyboardButton(
        text="❌ Отменить",
        callback_data="cancel_remove"
    )])

    await message.answer(
        "🗑️ Выберите репозиторий для удаления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@router.callback_query(F.data.startswith("remove:"))
async def remove_repo_callback(
    callback: CallbackQuery,
    user_repos: UserRepositories,
):
    user_id = callback.from_user.id
    repo_link = callback.data.replace("remove:", "")

    if user_repos.exists(user_id, repo_link):
        user_repos.remove(user_id, repo_link)
        await callback.message.edit_text(
            f"✅ Репозиторий удален:\n\n"
            f"• Ссылка: `{repo_link}`",
            parse_mode='Markdown'
        )
    else:
        await callback.message.edit_text("❌ Ошибка: репозиторий не найден")

    await callback.answer()


@router.callback_query(F.data == "cancel_remove")
async def cancel_remove(callback: CallbackQuery):
    await callback.message.edit_text("❌ Удаление отменено")
    await callback.answer()
