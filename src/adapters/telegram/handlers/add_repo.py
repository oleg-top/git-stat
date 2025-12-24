from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from adapters.telegram.keyboards.main import get_main_keyboard
from adapters.telegram.utils import is_valid_git_url
from app.use_cases.add_user_repository import AddUserRepositoryUseCase
from infra.git.exceptions import GitPullError, GitCloneError

router = Router()


class AddRepoStates(StatesGroup):
    waiting_for_link = State()


@router.message(F.text == "➕ Добавить репозиторий")
async def add_repo_start(message: types.Message, state: FSMContext):
    await message.answer(
        "📥 Пришлите ссылку на Git репозиторий:\n\n"
        "Примеры:\n"
        "• https://github.com/username/repo.git\n"
        "• git@github.com:username/repo.git\n\n"
        "❌ Для отмены отправьте /cancel"
    )
    await state.set_state(AddRepoStates.waiting_for_link)


@router.message(AddRepoStates.waiting_for_link, F.text)
async def add_repo_receive_link(
    message: types.Message,
    state: FSMContext,
    add_repo_uc: AddUserRepositoryUseCase,
):
    repo_link = message.text.strip()

    if message.text.lower() == "/cancel":
        await state.clear()
        await message.answer("❌ Добавление репозитория отменено")
        return

    if not is_valid_git_url(repo_link):
        await message.answer(
            "❌ Неверный формат ссылки!\n\n"
            "Поддерживаемые форматы:\n"
            "• https://github.com/user/repo.git\n"
            "• https://gitlab.com/user/repo.git\n"
            "• git@github.com:user/repo.git\n\n"
            "Попробуйте еще раз или отправьте /cancel для отмены:"
        )
        return

    user_id = message.from_user.id

    try:
        added = add_repo_uc.execute(user_id=user_id, repo_url=repo_link)
        if added:
            await message.answer(
                f"✅ Репозиторий успешно добавлен!\n\n"
                f"• Ссылка: `{repo_link}`\n\n"
                f"Теперь вы можете получить по нему статистику!",
                parse_mode='Markdown'
            )
        else:
            await message.answer(
                f"⚠️ Репозиторий уже был в вашем списке:\n\n"
                f"• Ссылка: `{repo_link}`",
                parse_mode='Markdown'
            )
    except (GitPullError, GitCloneError) as e:
        await message.answer("❌ Ошибка при добавлении репозитория")
        print(f"Error: {e}")

    await state.clear()


@router.message(Command("cancel"))
async def cancel_any_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Нет активных операций для отмены")
        return

    keyboard = get_main_keyboard()
    await state.clear()
    await message.answer(
        text="❌ Операция отменена",
        reply_markup=keyboard,
    )
