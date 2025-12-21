import io
import subprocess
from subprocess import CalledProcessError
from typing import TextIO


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
        print(e.stdout)
        print(e.stderr)
        exit(e.returncode)

    return io.StringIO(res.stdout)
