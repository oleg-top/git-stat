import io
import subprocess
from typing import TextIO


def run_log(
        repo_path: str,
        file_path: str,
        revision: str
) -> TextIO:
    res = subprocess.run(
        ["git", "log", revision, "--reverse", "--pretty=format:\"%H %ae %an\"", "--", file_path, "|", "head", "-1"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )

    return io.StringIO(res.stdout[1:-1])
