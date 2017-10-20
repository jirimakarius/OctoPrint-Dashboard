import os
import raven
from . import __version__


class Config:
    SENTRY_CONFIG = {
        'dsn': 'https://e074c578006141259e269ac5f7b54022:0578554a9ddf4c6e922c1168998987af@sentry.io/233051',
        'include_paths': ['octoprint_dashboard'],
        'release': raven.fetch_git_sha(os.path.dirname(os.path.dirname(__file__))) or "package v{}".format(__version__),
    }
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/database.db'.format(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "model", "migrations")