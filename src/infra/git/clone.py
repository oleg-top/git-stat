import os
import subprocess

from infra.git.exceptions import GitCloneError


def run_clone(repo_url: str, path_to_store: str) -> None:
    if not os.path.exists(path_to_store):
        os.makedirs(path_to_store, exist_ok=True)

    try:
        subprocess.run(
            ["git", "clone", repo_url, path_to_store],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise GitCloneError(f"Ошибка при клонировании репозитория: {e.stderr}")
