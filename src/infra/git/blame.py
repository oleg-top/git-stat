import io
import subprocess
from typing import TextIO


def run_blame(
        repo_path: str,
        file_path: str,
        revision: str
) -> TextIO:
    res = subprocess.run(
        ["git", "blame", "--incremental", file_path, revision],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )

    return io.StringIO(res.stdout)
