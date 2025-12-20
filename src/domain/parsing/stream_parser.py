from typing import Protocol

from domain.models.blame import BlameStream, BlameFileStream, BlameAuthorData, BlameHashLine, CommitHash
from domain.models.stats import StreamStats, AuthorData, AuthorStats


class StreamParser(Protocol):
    def get_stream_stats(self, stream: BlameStream) -> StreamStats:
        pass


class StreamFileParser:
    def __init__(self):
        self.__commits_to_author: dict[CommitHash, AuthorData] = {}
        self.__stats: StreamStats = {}

    def __add_commit(self, blame_author_data: BlameAuthorData) -> None:
        if blame_author_data.Author.Name not in self.__stats.keys():
            self.__stats[blame_author_data.Author.Name] = AuthorStats(
                Author=blame_author_data.Author,
                Lines=0,
                Commits=set(blame_author_data.Hash),
                Files=1,
            )
        else:
            self.__stats[blame_author_data.Author.Name].Commits.add(blame_author_data.Hash)

        self.__commits_to_author[blame_author_data.Hash] = blame_author_data.Author

    def get_stream_stats(self, stream: BlameFileStream) -> StreamStats:
        for blame_entry in stream:
            if isinstance(blame_entry, BlameAuthorData):
                self.__add_commit(blame_entry)
            elif isinstance(blame_entry, BlameHashLine):
                author_data = self.__commits_to_author[blame_entry.Hash]
                self.__stats[author_data.Name].Lines += blame_entry.LinesChanged

        return self.__stats
