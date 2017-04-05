from octoprint_dashboard.app import db


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth = db.Column(db.String(80))
    client_refresh = db.Column(db.Integer)
    server_refresh = db.Column(db.Integer)

    _config = None

    def __init__(self, auth, client_refresh, server_refresh):
        self.auth = auth
        self.client_refresh = client_refresh
        self.server_refresh = server_refresh

    def __repr__(self):
        return '<Config %r>' % self.id
