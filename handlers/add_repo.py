from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from services.redis_service import redis_client
from utils import is_valid_git_url

router = Router()


class AddRepoStates(StatesGroup):
    waiting_for_link = State()
    waiting_for_revision = State()


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
async def add_repo_receive_link(message: types.Message, state: FSMContext):
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

    await state.update_data(repo_link=repo_link)
    await message.answer(
        "📝 Теперь укажите ревизию (ветку, тег или хэш коммита):\n\n"
        "Примеры:\n"
        "• main\n"
        "• master\n"
        "• v1.0.0\n"
        "• abc123def\n\n"
        "По умолчанию будет использоваться 'main'\n"
        "❌ Для отмены отправьте /cancel"
    )
    await state.set_state(AddRepoStates.waiting_for_revision)


@router.message(AddRepoStates.waiting_for_revision, F.text)
async def add_repo_receive_revision(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    revision = message.text.strip() or "main"

    if message.text.lower() == "/cancel":
        await state.clear()
        await message.answer("❌ Добавление репозитория отменено")
        return

    user_data = await state.get_data()
    repo_link = user_data['repo_link']

    try:
        result = redis_client.add_repo(user_id, repo_link, revision)
        if result == 1:
            await message.answer(
                f"✅ Репозиторий успешно добавлен!\n\n"
                f"• Ссылка: `{repo_link}`\n"
                f"• Ревизия: `{revision}`\n\n"
                f"Теперь вы можете получить по нему статистику!",
                parse_mode='Markdown'
            )
        else:
            await message.answer(
                f"⚠️ Репозиторий уже был в вашем списке:\n\n"
                f"• Ссылка: `{repo_link}`\n"
                f"• Ревизия: `{revision}`",
                parse_mode='Markdown'
            )
    except Exception as e:
        await message.answer("❌ Ошибка при добавлении репозитория")
        print(f"Error: {e}")

    await state.clear()


@router.message(Command("cancel"))
async def cancel_any_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Нет активных операций для отмены")
        return

    await state.clear()
    await message.answer("❌ Операция отменена")
