from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from adapters.telegram.keyboards.main import get_main_keyboard
from app.use_cases.dummy_parse_repository import ParseRepositoryUseCase
from domain.models.filterer import ExtensionsFilter, ExclusionsFilter, RestrictionsFilter
from domain.models.user_repos import UserRepositories

router = Router()


class StatsStates(StatesGroup):
    waiting_for_repo = State()
    waiting_for_revision = State()
    waiting_for_filters = State()


def get_stats_repos_keyboard(repo_list: list[str]) -> types.ReplyKeyboardMarkup:
    buttons = [[types.KeyboardButton(text=repo)] for repo in repo_list]
    buttons.append([types.KeyboardButton(text="❌ Отменить")])
    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )


@router.message(F.text == "📊 Получить статистику")
async def stats_start(message: types.Message, state: FSMContext, user_repos: UserRepositories):
    user_id = message.from_user.id
    repos = user_repos.list(user_id)

    if not repos:
        await message.answer("📭 У вас нет репозиториев для анализа")
        return

    keyboard = get_stats_repos_keyboard(repos)
    await message.answer(
        "📂 Выберите репозиторий для анализа.\n"
        "Нажмите на репозиторий из списка ниже или отправьте /cancel для отмены:",
        reply_markup=keyboard
    )
    await state.set_state(StatsStates.waiting_for_repo)


@router.message(StatsStates.waiting_for_repo, F.text)
async def stats_receive_repo(
        message: types.Message,
        state: FSMContext,
        user_repos: UserRepositories
):
    user_id = message.from_user.id
    repo_link = message.text.strip()

    if repo_link.lower() == "/cancel" or repo_link == "❌ Отменить":
        keyboard = get_main_keyboard()
        await state.clear()
        await message.answer(
            "❌ Операция отменена",
            reply_markup=keyboard,
        )
        return

    if not user_repos.exists(user_id, repo_link):
        await message.answer("❌ У вас нет такого репозитория. Выберите из списка.")
        return

    await state.update_data(repo_link=repo_link)
    await message.answer(
        "📝 Укажите ревизию для анализа.\n"
        "Это может быть:\n"
        "• имя ветки (например: main, master)\n"
        "• тег (например: v1.0.0)\n"
        "• конкретный хэш коммита (например: abc123def)\n"
        "Если оставить пустым, будет использоваться 'HEAD'.\n"
        "❌ Для отмены отправьте /cancel"
    )
    await state.set_state(StatsStates.waiting_for_revision)


@router.message(StatsStates.waiting_for_revision, F.text)
async def stats_receive_revision(message: types.Message, state: FSMContext):
    revision = message.text.strip() or "HEAD"

    if revision.lower() == "/cancel":
        keyboard = get_main_keyboard()

        await state.clear()
        await message.answer(
            "❌ Операция отменена",
            reply_markup=keyboard,
        )
        return

    await state.update_data(revision=revision)
    await message.answer(
        "🔹 Укажите фильтры для анализа.\n"
        "Формат: несколько фильтров через точку с запятой (;)\n"
        "Поддерживаемые типы:\n"
        "1️⃣ Расширения файлов (ext) — через запятую, пример: ext:.py,.js\n"
        "2️⃣ Исключения (exc) — файлы/папки, которые не учитывать, пример: exc:tests/*,docs/*.md\n"
        "3️⃣ Ограничения (res) — только файлы/папки, которые учитывать, пример: res:src/*.py\n"
        "Полный пример: ext:.py,.cpp;exc:tests/*,docs/*.md;res:src/*.py\n"
        "❌ Для отмены отправьте /cancel"
    )
    await state.set_state(StatsStates.waiting_for_filters)


@router.message(StatsStates.waiting_for_filters, F.text)
async def stats_receive_filters(
        message: types.Message,
        state: FSMContext,
        parse_repo_uc: ParseRepositoryUseCase
):
    text = message.text.strip()

    if text.lower() == "/cancel":
        keyboard = get_main_keyboard()

        await state.clear()
        await message.answer(
            "❌ Операция отменена",
            reply_markup=keyboard,
        )
        return

    data = await state.get_data()
    repo_link = data['repo_link']
    revision = data['revision']

    parse_repo_uc.storage.set_revision(revision)
    parse_repo_uc.file_converter.set_revision(revision)

    filters = []

    sth = False
    for part in text.split(";"):
        part = part.strip()
        if part.startswith("ext:"):
            exts = {e.strip() for e in part[4:].split(",") if e.strip()}
            filters.append(ExtensionsFilter(exts))
            sth = True
        elif part.startswith("exc:"):
            excs = [e.strip() for e in part[4:].split(",") if e.strip()]
            filters.append(ExclusionsFilter(excs))
            sth = True
        elif part.startswith("res:"):
            res = [e.strip() for e in part[4:].split(",") if e.strip()]
            filters.append(RestrictionsFilter(res))
            sth = True

    if not sth:
        await message.answer("❌ Ошибка при разборе фильтров. Попробуйте снова.")
        return

    await message.answer("⏳ Считаем статистику, это может занять некоторое время...")

    try:
        stats = parse_repo_uc.execute(repository_url=repo_link, filters=filters)

        response = f"📊 Статистика для {repo_link} ({revision}):\n\n"
        for author, stat in stats.items():
            response += f"• {author}: {stat.Lines} строк, {stat.Files} файлов\n"

        await message.answer(response)
    except Exception as e:
        await message.answer("❌ Ошибка при подсчёте статистики")
        print(f"Error: {e}")

    keyboard = get_main_keyboard()
    await state.clear()
    await message.answer(
        "Выберите действие:",
        reply_markup=keyboard,
    )
