from flask_socketio import disconnect, join_room, emit
from jwt import DecodeError, ExpiredSignature

from octoprint_dashboard.app import socketio
from octoprint_dashboard.model import User, Printer, Group
from octoprint_dashboard.services import LoginService


@socketio.on('join')
def on_join(data):
    token = data.get('jwt')
    if not token:
        disconnect()
        return

    try:
        payload = LoginService.parse_api_token_direct(token)
    except DecodeError:
        disconnect()
        return
    except ExpiredSignature:
        disconnect()
        return
    printers = Printer.query.join(Printer.group).join(Group.group_user).filter(
        User.username == payload["username"]).all()

    for printer in printers:
        join_room(str(printer.id))
        print(printer.id)

    # socketio.emit("status", {"message": "fuck"}, room="1")
