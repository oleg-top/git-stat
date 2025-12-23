from domain.models.file_converter import FileConverter
from domain.models.filterer import RepositoryFilterer, RepositoryFilter, DefaultRepositoryFilterer, ExtensionsFilter
from domain.models.stats import RepoStats
from domain.models.storage import RepositoryStorage
from domain.parsing.repo_parser import RepoParser
from domain.parsing.stream_parser import StreamParser, StreamFileParser
from infra.git.file_converter import GitFileConverter
from infra.storage.local.storage import LocalGitRepositoryStorage


class ParseRepositoryUseCase:
    def __init__(
            self,
            storage: RepositoryStorage,
            file_converter: FileConverter,
            filterer: RepositoryFilterer,
            stream_parser: StreamParser,
    ) -> None:
        self.storage = storage
        self.file_converter = file_converter

        self.__filterer = filterer
        self.__stream_parser = stream_parser

    def execute(self, repository_url: str, filters: list[RepositoryFilter]) -> RepoStats:
        repository = self.storage.ensure(repository_url)

        self.__filterer.set(filters)
        filtered_repository = self.__filterer.apply(repository)

        repository_parser = RepoParser(
            filtered_repository,
            self.file_converter,
            self.__stream_parser,
        )

        return repository_parser.calculate_stats()


if __name__ == '__main__':
    storage = LocalGitRepositoryStorage()
    storage.set_revision("HEAD")
    file_converter = GitFileConverter("HEAD")
    filterer = DefaultRepositoryFilterer()
    stream_parser = StreamFileParser()
    dummy = ParseRepositoryUseCase(
        storage,
        file_converter,
        filterer,
        stream_parser
    )

    print(dummy.execute(
        "https://github.com/oleg-top/git-stat.git",
        [
            # ExtensionsFilter({".py"})
        ]
    ))
