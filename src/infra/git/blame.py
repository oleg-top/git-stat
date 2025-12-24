import io
import subprocess
from typing import TextIO

from infra.git.exceptions import GitBlameError


def run_blame(repo_path: str, file_path: str, revision: str) -> TextIO:
    try:
        res = subprocess.run(
            ["git", "blame", "--incremental", file_path, revision],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return io.StringIO(res.stdout)
    except subprocess.CalledProcessError as e:
        raise GitBlameError(f"Ошибка git blame для {file_path}@{revision}")
