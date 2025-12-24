from domain.models.file_converter import FileConverter
from domain.models.repo import Repository
from domain.models.stats import RepoStats
from domain.parsing.stream_parser import StreamParser


class RepoParser:
    def __init__(
            self,
            repository: Repository,
            file_converter: FileConverter,
            stream_parser: StreamParser,
    ) -> None:
        self.__stream_parser = stream_parser
        self.__converter = file_converter
        self.__repository = repository
        self.__stats: RepoStats = {}

    def calculate_stats(self) -> RepoStats:
        self.__stats = {}

        for file_path in self.__repository:
            stream = self.__converter.stream(
                repository_path=self.__repository.get_path(),
                file_path=file_path,
            )
            stream_stats = self.__stream_parser.get_stream_stats(stream)

            for author_name, author_stats in stream_stats.items():
                if author_name in self.__stats:
                    self.__stats[author_name].Lines += author_stats.Lines
                    self.__stats[author_name].Files += 1
                    self.__stats[author_name].Commits.update(author_stats.Commits)
                else:
                    self.__stats[author_name] = author_stats

        return self.__stats
