from octoprint_dashboard.app import db
from octoprint_dashboard.model import utils


class Config(db.Model):
    """
    Instance of this class equals single record of config in database
    Class behaves like repository of Config records

    There has to be only one record of Config in database otherwise application wouldn't work
    """
    OAUTH_CVUT = "oauth_cvut"
    NONE = "none"

    AUTH_CHOICES = (
        (OAUTH_CVUT, "ČVUT - OAuth"),
        (NONE, "None")
    )

    id = db.Column(db.Integer, primary_key=True)
    secret = db.Column(db.String(80))
    auth = db.Column(utils.ChoiceType(choices=AUTH_CHOICES), default=NONE, nullable=False)
    oauth_client_id = db.Column(db.String)
    oauth_client_secret = db.Column(db.String)
    oauth_redirect_uri = db.Column(db.String)

    def __init__(self, secret, auth, oauth_client_id, oauth_client_secret, oauth_redirect_uri):
        self.secret = secret
        self.auth = auth
        self.oauth_client_id = oauth_client_id
        self.oauth_client_secret = oauth_client_secret
        self.oauth_redirect_uri = oauth_redirect_uri

    def __repr__(self):
        return '<Config %r>' % self.id

    def load(self):
        return {
            "SECRET": self.secret,
            "AUTH": self.auth,
            "OAUTH_CLIENT_ID": self.oauth_client_id,
            "OAUTH_CLIENT_SECRET": self.oauth_client_secret,
            "OAUTH_REDIRECT_URI": self.oauth_redirect_uri,
            "OCTO_CONF": True
        }