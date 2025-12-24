import io
import subprocess
from subprocess import CalledProcessError
from typing import TextIO

from infra.git.exceptions import GitLSTreeError


def run_ls_tree(
        repo_path: str,
        revision: str,
) -> TextIO:
    try:
        res = subprocess.run(
            ["git", "ls-tree", "-r", revision, "--name-only"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )

    except CalledProcessError as e:
        raise GitLSTreeError(f"Ошибка при клонировании репозитория: {e.stderr}")

    return io.StringIO(res.stdout)
