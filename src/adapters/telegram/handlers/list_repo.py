from aiogram import Router, types, F
from domain.models.user_repos import UserRepositories

router = Router()


@router.message(F.text == "📂 Мои репозитории")
async def list_repos(
    message: types.Message,
    user_repos: UserRepositories,
):
    user_id = message.from_user.id

    repos = user_repos.list(user_id)

    if not repos:
        await message.answer("📭 Список репозиториев пуст")
        return

    response = "📂 Ваши репозитории:\n\n"
    for i, repo_link in enumerate(repos, 1):
        display_repo = repo_link
        response += f"{i}. {display_repo}\n"

    await message.answer(response)

