from domain.models.stats import RepoStats
from domain.models.storage import RepositoryStorage
from domain.parsing.repo_parser import RepoParser
from domain.parsing.stream_parser import StreamParser, StreamFileParser
from infra.storage.local.storage import LocalGitRepositoryStorage


class DummyParseRepositoryUseCase:
    def __init__(
            self,
            storage: RepositoryStorage,
            stream_parser: StreamParser,
    ) -> None:
        self.__storage = storage
        self.__stream_parser = stream_parser

    def execute(self, repository_url: str) -> RepoStats:
        repository = self.__storage.ensure(repository_url)
        repository_parser = RepoParser(self.__stream_parser, repository)

        return repository_parser.calculate_stats()


if __name__ == '__main__':
    storage = LocalGitRepositoryStorage()
    storage.set_restrictions(["*.py"])
    storage.set_revision("origin/master")
    stream_parser = StreamFileParser()
    dummy = DummyParseRepositoryUseCase(storage, stream_parser)

    print(dummy.execute("https://github.com/oleg-top/git-stat.git"))
