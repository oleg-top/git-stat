import subprocess


def run_pull(repo_path: str) -> None:
    subprocess.run(
        ["git", "pull","--force", "--no-rebase", "--no-edit"],
        cwd=repo_path,
        check=True,
    )
