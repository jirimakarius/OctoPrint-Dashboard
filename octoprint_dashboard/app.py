from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  # allows cross-origin requests
db = SQLAlchemy(app)  # create database connection
import octoprint_dashboard.model

db.create_all()  # creates database schema

from octoprint_dashboard.background import Scheduler, ZeroconfBrowser

scheduler = Scheduler()
zeroconf_browser = ZeroconfBrowser()
import octoprint_dashboard.cli_commands

import octoprint_dashboard.login.routes
import octoprint_dashboard.api


def shutdown_server():
    """
    Function for stopping server
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.before_first_request
def _startup():
    """
    Function executed before first request, checks if is application configured
    and at least one superadmin present, if not shutdowns server
    """
    from octoprint_dashboard.model import User, Config
    if Config.query.scalar() is None:
        print("No config, add config via command 'python -m flask config'")
        shutdown_server()
    if User.query.filter_by(superadmin=True).count() == 0:
        print("No superadmin, add superadmin via command 'python -m flask add_superadmin <username>'")
        shutdown_server()

    scheduler.start()  # starts background task scheduler
    zeroconf_browser.start()  # starts MDNS service discovery


@app.route('/')
@app.route('/admin')
def index():
    return send_from_directory('dist', 'index.html')


@app.route('/<text>.js')
def javascript(text):
    return send_from_directory('dist', text + ".js")
