import pytest
from typing import Iterator

from domain.models.filterer import ExtensionsFilter, ExclusionsFilter, RestrictionsFilter, DefaultRepositoryFilterer
from domain.models.repo import RepositoryPath, RepositoryFilePath


class DummyRepository:
    def __init__(self, files: list[str]):
        self._files = files

    def get_path(self) -> RepositoryPath:
        return "/repo"

    def __iter__(self) -> Iterator[RepositoryFilePath]:
        yield from self._files


def test_extensions_filter_matches_allowed_extension():
    f = ExtensionsFilter({".py", ".cpp"})

    assert f.match("main.py") is True
    assert f.match("main.cpp") is True


def test_extensions_filter_rejects_other_extensions():
    f = ExtensionsFilter({".py"})

    assert f.match("README.md") is False
    assert f.match("script.sh") is False


def test_extensions_filter_cache_key():
    f = ExtensionsFilter({".py", ".cpp"})
    key = f.cache_key

    assert key.startswith("ext:")
    assert ".py" in key
    assert ".cpp" in key


def test_exclusions_filter_excludes_matching_paths():
    f = ExclusionsFilter(["tests/*", "docs/*.md"])

    assert f.match("tests/test_app.py") is False
    assert f.match("docs/readme.md") is False


def test_exclusions_filter_allows_non_matching_paths():
    f = ExclusionsFilter(["tests/*"])

    assert f.match("src/main.py") is True


def test_exclusions_filter_cache_key():
    f = ExclusionsFilter(["tests/*", "docs/*"])
    key = f.cache_key

    assert key == "exc:tests/*,docs/*"


def test_restrictions_filter_allows_only_matching_paths():
    f = RestrictionsFilter(["src/*.py"])

    assert f.match("src/main.py") is True
    assert f.match("tests/test_main.py") is False


def test_restrictions_filter_multiple_patterns_all_must_match():
    f = RestrictionsFilter(["src/*", "*.py"])

    assert f.match("src/main.py") is True
    assert f.match("src/main.js") is False


def test_restrictions_filter_cache_key():
    f = RestrictionsFilter(["src/*.py"])
    assert f.cache_key == "exc:src/*.py"


def test_filterer_without_filters_returns_all_files():
    repo = DummyRepository([
        "src/main.py",
        "README.md",
        "tests/test_main.py",
    ])

    filterer = DefaultRepositoryFilterer()
    filterer.set([])

    filtered = list(filterer.apply(repo))

    assert filtered == [
        "src/main.py",
        "README.md",
        "tests/test_main.py",
    ]


def test_filterer_applies_single_filter():
    repo = DummyRepository([
        "src/main.py",
        "README.md",
        "tests/test_main.py",
    ])

    filterer = DefaultRepositoryFilterer()
    filterer.set([ExtensionsFilter({".py"})])

    filtered = list(filterer.apply(repo))

    assert filtered == [
        "src/main.py",
        "tests/test_main.py",
    ]


def test_filterer_applies_multiple_filters_and_logic():
    repo = DummyRepository([
        "src/main.py",
        "src/main.cpp",
        "tests/test_main.py",
    ])

    filterer = DefaultRepositoryFilterer()
    filterer.set([
        ExtensionsFilter({".py"}),
        ExclusionsFilter(["tests/*"]),
    ])

    filtered = list(filterer.apply(repo))

    assert filtered == ["src/main.py"]


def test_filterer_does_not_modify_original_repository():
    repo = DummyRepository(["a.py", "b.md"])

    filterer = DefaultRepositoryFilterer()
    filterer.set([ExtensionsFilter({".py"})])

    _ = list(filterer.apply(repo))

    assert list(repo) == ["a.py", "b.md"]
