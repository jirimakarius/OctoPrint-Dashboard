import eventlet
from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from os import path

eventlet.monkey_patch()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/database.db'.format(path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MIGRATIONS_DIR"] = path.join(path.dirname(__file__), "model", "migrations")
CORS(app)  # allows cross-origin requests
db = SQLAlchemy(app)  # create database connection
socketio = SocketIO(app, async_mod="eventlet")
import octoprint_dashboard.model

migrate = Migrate(app, db, directory=app.config["MIGRATIONS_DIR"])
with app.app_context():
    upgrade(directory=app.config["MIGRATIONS_DIR"])

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

    from octoprint_dashboard.services import LoginService
    LoginService.init()
    zeroconf_browser.start()  # starts MDNS service discovery
    octoprint_status.start()


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
