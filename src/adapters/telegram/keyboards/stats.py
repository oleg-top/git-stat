from aiogram import types


def get_stats_repos_keyboard(repo_list: list[str]) -> types.ReplyKeyboardMarkup:
    buttons = [[types.KeyboardButton(text=repo)] for repo in repo_list]
    buttons.append([types.KeyboardButton(text="❌ Отменить")])

    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )