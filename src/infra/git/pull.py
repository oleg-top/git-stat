import subprocess


def run_pull(repo_path: str) -> None:
    subprocess.run(
        ["git", "pull"],
        cwd=repo_path,
        check=True,
    )
