import re
from typing import Optional, List, Dict, Any


def is_valid_git_url(url: Optional[str]) -> bool:
    if url is None:
        return False

    patterns = [
        r'^https?://github\.com/[\w\.\-]+/[\w\.\-]+(\.git)?$',
        r'^https?://gitlab\.com/[\w\.\-]+/[\w\.\-]+(\.git)?$',
        r'^https?://bitbucket\.org/[\w\.\-]+/[\w\.\-]+(\.git)?$',

        r'^git@github\.com:[\w\.\-]+/[\w\.\-]+(\.git)?$',
        r'^git@gitlab\.com:[\w\.\-]+/[\w\.\-]+(\.git)?$',

        r'^https?://github\.com/[\w\.\-]+/[\w\.\-]+$',
        r'^https?://gitlab\.com/[\w\.\-]+/[\w\.\-]+$',
    ]

    try:
        url = url.strip()
    except AttributeError:
        return False

    if not url.endswith('.git') and re.match(r'^https?://(github|gitlab)\.com/', url):
        url += '.git'

    return any(re.match(pattern, url) for pattern in patterns)


def format_repo_list(repos):
    try:
        iter(repos)
    except TypeError:
        return "📭 Список репозиториев пуст"

    if not repos:
        return "📭 Список репозиториев пуст"

    message = "📂 Ваши репозитории:\n\n"
    for i, repo_data in enumerate(repos, 1):

        if not isinstance(repo_data, dict):
            continue

        repo_link = repo_data.get('link', '')
        revision = repo_data.get('revision', 'main')

        if len(repo_link) > 50:
            display_repo = repo_link[:47] + "..."
        else:
            display_repo = repo_link

        message += f"{i}. {display_repo}\n"
        message += f"   Ревизия: {revision}\n\n"

    if message == "📂 Ваши репозитории:\n\n":
        return "📭 Список репозиториев пуст"

    return message
