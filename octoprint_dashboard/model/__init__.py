from .User import User
from octoprint_dashboard import app, db
import click


@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Init the db')
