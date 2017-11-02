#from .web import run_server
#from .cli import list_repos, list_labels, run
from .labelord import cli, app

__all__ = ['cli', 'app']