import os
import subprocess


def run_clone(repo_url: str, path_to_store: str) -> None:
    if not os.path.exists(path_to_store):
        os.makedirs(path_to_store, exist_ok=True)

    res = subprocess.run(
        ["git", "clone", repo_url, path_to_store],
        capture_output=True,
        text=True,
        check=True,
    )

    # TODO: когда-то надо добавить логирование