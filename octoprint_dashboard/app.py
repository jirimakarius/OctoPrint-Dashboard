import eventlet
from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from .config import Config

eventlet.monkey_patch()
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # allows cross-origin requests
socketio = SocketIO(app, async_mod="eventlet")
sentry = Sentry(app, dsn='https://e074c578006141259e269ac5f7b54022:0578554a9ddf4c6e922c1168998987af@sentry.io/233051')
db = SQLAlchemy(app)  # create database connection
migrate = Migrate(app, db, directory=app.config["MIGRATIONS_DIR"])


def shutdown_server(message):
    """
    Function for stopping server
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError(message)
    func()


from octoprint_dashboard.background import ZeroconfBrowser, OctoprintStatus

zeroconf_browser = ZeroconfBrowser()
octoprint_status = OctoprintStatus()

with app.app_context():
    upgrade(directory=app.config["MIGRATIONS_DIR"])

    from octoprint_dashboard.services import LoginService

    LoginService.init()
    zeroconf_browser.start()  # starts MDNS service discovery
    octoprint_status.start()


@app.before_first_request
def _startup():
    """
    Function executed before first request, checks if is application configured
    and at least one superadmin present, if not shutdowns server
    """
    from octoprint_dashboard.model import User, Config

    if Config.query.scalar() is None:
        print("No config, add config via command 'python -m flask config'")
        shutdown_server("No config, add config via command 'python -m flask config'")
    if User.query.filter_by(superadmin=True).count() == 0:
        print("No superadmin, add superadmin via command 'python -m flask add_superadmin <username>'")
        shutdown_server("No superadmin, add superadmin via command 'python -m flask add_superadmin <username>'")


import octoprint_dashboard.cli_commands
import octoprint_dashboard.login.routes
import octoprint_dashboard.api
import octoprint_dashboard.socketIO.socketioService


@app.route('/')
@app.route('/admin')
def index():
    return send_from_directory('dist', 'index.html')


@app.route('/<text>.js')
def javascript(text):
    return send_from_directory('dist', text + ".js")
