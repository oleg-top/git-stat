from domain.models.storage import RepositoryStorage
from domain.models.user_repos import UserRepositories


class AddUserRepositoryUseCase:
    def __init__(
        self,
        user_repository: UserRepositories,
        repository_storage: RepositoryStorage,
    ) -> None:
        self.__user_repository = user_repository
        self.__repo_storage = repository_storage

    def execute(self, user_id: int, repo_url: str) -> bool:
        if self.__user_repository.exists(user_id, repo_url):
            return False

        self.__repo_storage.ensure(repo_url)
        self.__user_repository.add(user_id, repo_url)

        return True