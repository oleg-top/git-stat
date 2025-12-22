from typing import List, Dict, Any


class RedisService:

    def __init__(self):
        self._data = {}
        print("🗄️  Redis service initialized (in-memory storage)")

    def add_repo(self, user_id: int, repo_link: str, revision: str = "main") -> int:
        key = f"user:{user_id}:repos"
        if key not in self._data:
            self._data[key] = []

        for repo in self._data[key]:
            if repo['link'] == repo_link and repo['revision'] == revision:
                return 0

        self._data[key].append({
            'link': repo_link,
            'revision': revision
        })
        return 1

    def remove_repo(self, user_id: int, repo_link: str, revision: str = "main") -> int:
        key = f"user:{user_id}:repos"
        if key in self._data:
            for i, repo in enumerate(self._data[key]):
                if repo['link'] == repo_link and repo['revision'] == revision:
                    del self._data[key][i]
                    return 1
        return 0

    def get_repos(self, user_id: int) -> List[Dict[str, Any]]:
        key = f"user:{user_id}:repos"
        return self._data.get(key, [])

    def get_repo(self, user_id: int, repo_link: str, revision: str = "main") -> Dict[str, Any] | None:
        key = f"user:{user_id}:repos"
        if key in self._data:
            for repo in self._data[key]:
                if repo['link'] == repo_link and repo['revision'] == revision:
                    return repo
        return None

    def repo_exists(self, user_id: int, repo_link: str, revision: str = "main") -> bool:
        return self.get_repo(user_id, repo_link, revision) is not None


redis_client = RedisService()
