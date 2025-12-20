from dataclasses import dataclass
from typing import Protocol, Iterator, TextIO, TypeAlias
from stats import AuthorData


class BlameEntry:
    pass


CommitHash: TypeAlias = str


@dataclass(frozen=True)
class BlameHashLine(BlameEntry):
    Hash: CommitHash
    OriginalLine: int
    FinalLine: int
    LinesChanged: int


@dataclass(frozen=True)
class BlameAuthorData(BlameEntry):
    Author: AuthorData
    Commiter: AuthorData
    CommitMessage: str
    Hash: CommitHash


class BlameStream(Protocol):
    def __iter__(self) -> Iterator[BlameEntry]:
        pass


class BlameFileStream:
    def __init__(self, file: TextIO) -> None:
        self.__file = file
        self.__known_hashes: set[CommitHash] = set()

    def __iter__(self) -> Iterator[BlameEntry]:
        for line in self.__file:
            line_elements = line.split()
            if len(line_elements) != 4:
                continue

            commit_hash = line_elements[0]
            original_line = int(line_elements[1])
            final_line = int(line_elements[2])
            lines_changed = int(line_elements[3])

            if commit_hash not in self.__known_hashes:
                author = ''.join(next(self.__file).split()[1:])
                author_email = ''.join(next(self.__file).split()[1:])

                for _ in range(2):
                    next(self.__file)

                commiter = ''.join(next(self.__file).split()[1:])
                commiter_email = ''.join(next(self.__file).split()[1:])

                for _ in range(2):
                    next(self.__file)

                commit_message = ''.join(next(self.__file).split()[1:])

                yield BlameAuthorData(
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