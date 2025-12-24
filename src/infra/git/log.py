import io
import subprocess
from typing import TextIO

from infra.git.exceptions import GitLogError


def run_log(
        repo_path: str,
        file_path: str,
        revision: str
) -> TextIO:
    try:
        res = subprocess.run(
            ["git", "log", revision, "--reverse", "--pretty=format:\"%H %ae %an\"", "--", file_path, "|", "head", "-1"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise GitLogError(f"Ошибка при клонировании репозитория: {e.stderr}")

    return io.StringIO(res.stdout[1:-2])
