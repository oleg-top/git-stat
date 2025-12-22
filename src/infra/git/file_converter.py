from typing import Optional, TextIO

from domain.models.blame import CommitHash, BlameStream, BlameFileAuthorData, BlameCommitAuthorData, BlameHashLine
from domain.models.repo import RepositoryFilePath, RepositoryPath
from domain.models.stats import AuthorData
from infra.git.blame import run_blame
from infra.git.log import run_log


class GitFileConverter:
    def __init__(self, revision: Optional[str] = None) -> None:
        self.__revision: str = revision if revision is not None else "HEAD"
        self.__known_hashes: set[CommitHash] = set()

    @staticmethod
    def __file_is_empty(file: TextIO):
        if file.read(1) == "":
            file.seek(0)

            return True

        file.seek(0)

        return False

    def stream(
            self,
            repository_path: RepositoryPath,
            file_path: RepositoryFilePath,
    ) -> BlameStream:
        blame = run_blame(
            repo_path=repository_path,
            file_path=file_path,
            revision=self.__revision,
        )

        self.__known_hashes = set()

        if self.__file_is_empty(blame):
            log = run_log(
                repo_path=repository_path,
                file_path=file_path,
                revision=self.__revision,
            )

            line_elements = log.readline().split()
            commit_hash = line_elements[0]
            author_email = line_elements[1]
            author_name = ' '.join(line_elements[2:])

            yield BlameFileAuthorData(
                Author=AuthorData(
                    Name=author_name,
                    Email=author_email,
                ),
                Hash=commit_hash,
            )

        for line in blame:
            line = line.strip()

            line_elements = line.split()
            if len(line_elements) != 4 or len(line_elements) > 0 and len(line_elements[0]) != 40:
                continue

            commit_hash = line_elements[0]
            original_line = int(line_elements[1])
            final_line = int(line_elements[2])
            lines_changed = int(line_elements[3])

            if commit_hash not in self.__known_hashes:
                author = ' '.join(next(blame).split()[1:])
                author_email = ' '.join(next(blame).split()[1:])

                for _ in range(2):
                    next(blame)

                commiter = ' '.join(next(blame).split()[1:])
                commiter_email = ' '.join(next(blame).split()[1:])

                for _ in range(2):
                    next(blame)

                commit_message = ' '.join(next(blame).split()[1:])

                self.__known_hashes.add(commit_hash)

                yield BlameCommitAuthorData(
                    Author=AuthorData(
                        Name=author,
                        Email=author_email,
                    ),
                    Commiter=AuthorData(
                        Name=commiter,
                        Email=commiter_email,
                    ),
                    CommitMessage=commit_message,
                    Hash=commit_hash,
                )

            yield BlameHashLine(
                Hash=commit_hash,
                OriginalLine=original_line,
                FinalLine=final_line,
                LinesChanged=lines_changed,
            )