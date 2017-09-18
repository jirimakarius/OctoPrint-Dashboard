import click

from octoprint_dashboard.app import app, db
from octoprint_dashboard.model import User, Config


@app.cli.command()
def dropdb():
    """
    Command for dropping database
    'flask dropdb'
    """
    db.drop_all()
    click.echo('Dropping the db')


@app.cli.command()
@click.argument('username')
def add_superadmin(username):
    """
    Command for adding superadmin via command line
    'flask add_superadmin <username>'
    """
    User.upsert_superadmin(username)
    click.echo('Powering up ' + username + ' to superadmin')


@app.cli.command()
def config():
    """
    Command for configuring application
    'flask config'
    """
    secret = input('Password for token encryption: ')
    oauth_client_id = input('Client ID for OAuth: ')
    oauth_client_secret = input('Client secret for OAuth: ')
    oauth_redirect_uri = input('Redirect URI for OAuth: ')
    config = Config.query.scalar()
    if config is None:
        config = Config(None, None, None, None)
        db.session.add(config)
    config.secret = secret
    config.oauth_client_id = oauth_client_id
    config.oauth_client_secret = oauth_client_secret
    config.oauth_redirect_uri = oauth_redirect_uri

    db.session.commit()
