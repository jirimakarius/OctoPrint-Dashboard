import eventlet
from flask import Flask, send_from_directory, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from .config import Config, ConfigForm

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
    from octoprint_dashboard.model import Config as ConfigDb

    LoginService.init()
    zeroconf_browser.start()  # starts MDNS service discovery
    octoprint_status.start()

    conf = ConfigDb.query.scalar()
    if conf:
        app.config.update(conf.load())


from octoprint_dashboard.socketIO import socketio_bp
from octoprint_dashboard.api import api_bp
from octoprint_dashboard.login import login_bp

app.register_blueprint(socketio_bp)
app.register_blueprint(api_bp)
app.register_blueprint(login_bp)


@app.before_request
def config_middleware():
    if not app.config.get("OCTO_CONF", False):
        from octoprint_dashboard.model import Config, User

        if request.method == "POST":
            form = ConfigForm(request.form)
            if form.valid:
                config = Config.query.scalar()
                if config is None:
                    config = Config(None, Config.NONE, None, None, None)
                    db.session.add(config)
                config.secret = form.secret
                config.auth = form.auth
                config.oauth_client_id = form.oauth_id
                config.oauth_client_secret = form.oauth_secret
                config.oauth_redirect_uri = form.oauth_uri
                db.session.commit()

                User.upsert_superadmin(form.admin)

                app.config.update(config.load())
                return redirect(url_for("index"))
            else:
                return render_template("config.html", auth_options=Config.AUTH_CHOICES, form=form)
        return render_template("config.html", auth_options=Config.AUTH_CHOICES)
    return None


@app.route('/')
@app.route('/admin')
def index():
    return send_from_directory('dist', 'index.html')


@app.route('/<text>.js')
def javascript(text):
    return send_from_directory('dist', text + ".js")
