from octoprint_dashboard.app import db


class Config(db.Model):
    """
    Instance of this class equals single record of config in database
    Class behaves like repository of Config records

    There has to be only one record of Config in database otherwise application wouldn't work
    """
    id = db.Column(db.Integer, primary_key=True)
    secret = db.Column(db.String(80))
    oauth_client_id = db.Column(db.String)
    oauth_client_secret = db.Column(db.String)
    oauth_redirect_uri = db.Column(db.String)

    def __init__(self, secret, oauth_client_id, oauth_client_secret, oauth_redirect_uri):
        self.secret = secret
        self.oauth_client_id = oauth_client_id
        self.oauth_client_secret = oauth_client_secret
        self.oauth_redirect_uri = oauth_redirect_uri

    def __repr__(self):
        return '<Config %r>' % self.id
