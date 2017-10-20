from flask import Blueprint

socketio_bp = Blueprint('socketio', __name__)

from . import socketioService
