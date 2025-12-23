from .start import router as start_router
from .add_repo import router as add_repo_router
from .list_repo import router as list_repo_router
from .remove_repo import router as remove_repo_router
from .common import router as common_router
from .stats import router as stats_router

__all__ = [
    'start_router',
    'add_repo_router',
    'list_repo_router',
    'remove_repo_router',
    'common_router',
    'stats_router'
]
