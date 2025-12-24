from domain.models.file_converter import FileConverter
from domain.models.filterer import RepositoryFilterer, RepositoryFilter, DefaultRepositoryFilterer, ExtensionsFilter
from domain.models.stats import RepoStats
from domain.models.stats_cache import StatsCache, make_stats_cache_key, RepositoryStatsCacheKey
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
            stats_cache: StatsCache,
    ) -> None:
        self.storage = storage
        self.file_converter = file_converter
        self.stats_cache = stats_cache

        self.__filterer = filterer
        self.__stream_parser = stream_parser

    def execute(self, repository_url: str, revision: str, filters: list[RepositoryFilter]) -> RepoStats:
        repository = self.storage.ensure(repository_url)
        key = make_stats_cache_key(
            RepositoryStatsCacheKey(
                repository_url,
                revision,
                tuple(sorted(f.cache_key for f in filters))
            )
        )

        cached = self.stats_cache.get(key)

        if cached is not None:
            return cached

        self.__filterer.set(filters)
        filtered_repository = self.__filterer.apply(repository)

        repository_parser = RepoParser(
            filtered_repository,
            self.file_converter,
            self.__stream_parser,
        )

        stats = repository_parser.calculate_stats()
        self.stats_cache.set(key, stats)

        return stats


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
