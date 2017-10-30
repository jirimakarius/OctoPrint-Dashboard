import os

import raven

from . import __version__


class Config:
    try:
        release = "development-" + raven.fetch_git_sha(os.path.dirname(os.path.dirname(__file__)))
    except:
        release = "package v{}".format(__version__)

    SENTRY_CONFIG = {
        'dsn': 'https://e074c578006141259e269ac5f7b54022:0578554a9ddf4c6e922c1168998987af@sentry.io/233051',
        'include_paths': ['octoprint_dashboard'],
        'release': release,
    }
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
        os.getenv("FLASK_DB", os.path.dirname(os.path.dirname(__file__)) + "/octoprint_dashboard.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "model", "migrations")


class ConfigForm:
    def __init__(self, formdata):
        self.secret = formdata.get("secret")
        self.auth = formdata.get("auth")
        self.oauth_id = formdata.get("oauth_id")
        self.oauth_secret = formdata.get("oauth_secret")
        self.oauth_uri = formdata.get("oauth_uri")
        self.admin = formdata.get("superadmin")

        self.errors = {}

        self.check()

    def check_string(self, attribute):
        val = getattr(self, attribute)

        if val:
            try:
                str(val)
            except:
                self.errors[attribute] = "Not string"
        else:
            self.errors[attribute] = "Required"

    def check_auth(self):
        from octoprint_dashboard.model import Config as ConfigDB

        if self.auth:
            try:
                str(self.auth)
                choices = [x[0] for x in ConfigDB.AUTH_CHOICES]
                if self.auth in choices:
                    return True
                else:
                    self.errors["auth"] = "Invalid option"
            except:
                self.errors["auth"] = "Invalid format"
        else:
            self.errors["auth"] = "Required"

        return False

    def check(self):
        from octoprint_dashboard.model import Config as ConfigDB

        self.check_string("secret")
        if self.check_auth():
            if self.auth != ConfigDB.NONE:
                self.check_string("oauth_id")
                self.check_string("oauth_secret")
                self.check_string("oauth_uri")
                self.check_string("admin")

    @property
    def valid(self):
        return len(self.errors) == 0
