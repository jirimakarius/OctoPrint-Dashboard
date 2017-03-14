from octoprint_dashboard import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    access_token = db.Column(db.String(80))
    refresh_token = db.Column(db.String(80))

    def __init__(self, username, access_token, refresh_token):
        self.username = username
        self.access_token = access_token
        self.refresh_token = refresh_token

    def __repr__(self):
        return '<User %r>' % self.username
