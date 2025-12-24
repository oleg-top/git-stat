class GitError(Exception):
    pass

class GitCloneError(GitError):
    pass

class GitPullError(GitError):
    pass

class GitBlameError(GitError):
    pass

class GitLSTreeError(GitError):
    pass

class GitLogError(GitError):
    pass
