import io
import os.path
from pathlib import Path
from typing import Iterator

from domain.models.blame import BlameStream, BlameFileStream
from domain.models.repo import RepoPath
from infra.git.blame import run_blame
from infra.git.log import run_log
from infra.git.ls_tree import run_ls_tree


class GitRepository:
    def __init__(
            self,
            repo_path: str,
            revision: str,
            extensions: set[str],
            exclude: list[str],
            restrict_to: list[str],
    ) -> None:
        self.__repo_path = repo_path
        self.__revision = revision
        self.__extensions = extensions
        self.__exclude = exclude
        self.__restrict_to = restrict_to

    def get_path(self) -> RepoPath:
        return self.__repo_path

    def __iter__(self) -> Iterator[BlameStream]:
        files = run_ls_tree(
            repo_path=self.__repo_path,
            revision=self.__revision,
        )

        # TODO: replace straight conditions with some filters structs
        for file in files:
            filepath = Path(file.strip())

            if len(self.__extensions) > 0:
                ext = filepath.suffix
                if ext not in self.__extensions:
                    continue

            if len(self.__exclude) > 0:
                to_exclude: bool = False

                for pattern in self.__exclude:
                    if filepath.match(pattern):
                        to_exclude = True
                        break

                if to_exclude:
                    continue

            if len(self.__restrict_to) > 0:
                restrict: bool = True

                for pattern in self.__restrict_to:
                    if not filepath.match(pattern):
                        restrict = False
                        break

                if not restrict:
                    continue

            blame = run_blame(
                repo_path=self.__repo_path,
                file_path=file.strip(),
                revision=self.__revision,
            )

            if blame.read(1) == "":
                blame.seek(0)

                log = run_log(
                    repo_path=self.__repo_path,
                    file_path=file.strip(),
                    revision=self.__revision,
                )

                yield BlameFileStream(io.StringIO(""), log)
            else:
                blame.seek(0)

                yield BlameFileStream(blame)
