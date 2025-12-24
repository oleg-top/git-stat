import subprocess

from infra.git.exceptions import GitPullError


def run_pull(repo_path: str) -> None:
    try:
        subprocess.run(
            ["git", "pull","--force", "--no-rebase", "--no-edit"],
            cwd=repo_path,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise GitPullError(f"Ошибка при клонировании репозитория: {e.stderr}")

