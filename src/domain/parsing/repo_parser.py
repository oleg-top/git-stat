from domain.models.repo import Repository
from domain.models.stats import RepoStats
from domain.parsing.stream_parser import StreamParser


class RepoParser:
    def __init__(self, stream_parser: StreamParser, repository: Repository):
        self.__stream_parser = stream_parser
        self.__repository = repository
        self.__stats: RepoStats = {}

    def calculate_stats(self) -> RepoStats:
        for stream in self.__repository:
            stream_stats = self.__stream_parser.get_stream_stats(stream)

            for author_name, author_stats in stream_stats.items():
                if author_name in self.__stats:
                    self.__stats[author_name].Lines += author_stats.Lines
                    self.__stats[author_name].Files += 1
                    self.__stats[author_name].Commits.update(author_stats.Commits)

        return self.__stats
