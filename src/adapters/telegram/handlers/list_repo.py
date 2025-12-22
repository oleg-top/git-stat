from aiogram import Router, types, F

from adapters.telegram.services.redis_service import redis_client

router = Router()


@router.message(F.text == "📂 Мои репозитории")
async def list_repos(message: types.Message):
    user_id = message.from_user.id

    try:
        repos = redis_client.get_repos(user_id)

        if not repos:
            await message.answer("📭 Список репозиториев пуст")
            return

        response = "📂 Ваши репозитории:\n\n"
        for i, repo_data in enumerate(repos, 1):
            repo_link = repo_data.get('link', '')
            revision = repo_data.get('revision', 'main')

            if len(repo_link) > 50:
                display_repo = repo_link[:47] + "..."
            else:
                display_repo = repo_link

            response += f"{i}. {display_repo}\n"
            response += f"   Ревизия: {revision}\n\n"

        await message.answer(response[:4000])

    except Exception as e:
        await message.answer("❌ Ошибка при получении списка репозиториев")
        print(f"Error: {e}")
