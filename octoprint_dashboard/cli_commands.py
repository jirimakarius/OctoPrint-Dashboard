import click
from octoprint_dashboard import app, db
from octoprint_dashboard.model import User


@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Init the db')


@app.cli.command()
@click.argument('username')
def add_superadmin(username):
    User.upsert_superadmin(username)
    click.echo('Powering up ' + username + ' to superadmin')
