from octoprint_dashboard.app import db


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secret = db.Column(db.String(80))
    client_refresh = db.Column(db.Integer)
    server_refresh = db.Column(db.Integer)
    oauth_client_id = db.Column(db.String)
    oauth_client_secret = db.Column(db.String)
    oauth_redirect_uri = db.Column(db.String)

    def __init__(self, secret, client_refresh, server_refresh, oauth_client_id, oauth_client_secret, oauth_redirect_uri):
        self.secret = secret
        self.client_refresh = client_refresh
        self.server_refresh = server_refresh
        self.oauth_client_id = oauth_client_id
        self.oauth_client_secret = oauth_client_secret
        self.oauth_redirect_uri = oauth_redirect_uri

    def __repr__(self):
        return '<Config %r>' % self.id
