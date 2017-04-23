from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "something"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)
import octoprint_dashboard.model
db.create_all() # default config přidat

from octoprint_dashboard.background import Scheduler, ZeroconfBrowser
scheduler = Scheduler()
zeroconf_browser = ZeroconfBrowser()
import octoprint_dashboard.cli_commands

import octoprint_dashboard.login.routes
import octoprint_dashboard.api


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.before_first_request
def _startup():
    from octoprint_dashboard.model import User, Config
    if Config.query.scalar() is None:
        print("No config, add config via command 'flask config'")
        shutdown_server()
    if User.query.filter_by(superadmin=True).scalar() is None:
        print("No superadmin, add superadmin via command 'flask add_superadmin <username>'")
        shutdown_server()

    scheduler.start()
    zeroconf_browser.start()


@app.route('/')
@app.route('/admin')
def frontend():
    return send_from_directory('dist', 'index.html')


@app.route('/<text>.js')
def neco(text):
    return send_from_directory('dist', text + ".js")
