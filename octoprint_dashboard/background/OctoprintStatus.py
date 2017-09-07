import json
from threading import Thread

import websocket
from eventlet import sleep
from octoclient import WebSocketEventHandler

from octoprint_dashboard.app import socketio
from octoprint_dashboard.model import Printer


class OctoprintDashboardEventHandler(WebSocketEventHandler):
    def run_with_id(self, printer_id):
        """
        Runs thread, which listens on socket.
        Executes given callbacks on events
        """

        def on_message(ws, data):
            if data.startswith('m'):
                self.on_message(ws, json.loads(data[1:]))
            elif data.startswith('a'):
                for msg in json.loads(data[1:]):
                    self.on_message(ws, msg, printer_id)

        def on_error(ws, exception):
            data = {
                "id": printer_id,
                "state": {
                    "text": "Offline/Unreachable"
                }
            }
            socketio.emit("status", data, room=str(printer_id))

        self.socket = websocket.WebSocketApp(self.url,
                                             on_open=self.on_open,
                                             on_close=self.on_close,
                                             on_message=on_message,
                                             on_error=on_error)
        self.thread = Thread(target=self.run_forever)
        self.thread.daemon = True
        self.thread.start()

    def run_forever(self):
        while True:
            self.socket.run_forever()
            sleep(5)


def on_message(ws, message, printer_id):
    if message.get("current"):
        data = message.get("current")
        data["id"] = printer_id
        socketio.emit("status", data, room=str(printer_id))


class OctoprintStatus:
    def __init__(self):
        printers = Printer.query.all()
        self.listeners = {}
        for printer in printers:
            listener = OctoprintDashboardEventHandler(printer.url, on_message=on_message)
            listener.run_with_id(printer.id)
            self.listeners[printer.id] = listener

    def add_listener(self, printer):
        listener = OctoprintDashboardEventHandler(printer.url, on_message=on_message)
        listener.run_with_id(printer.id)
        self.listeners[printer.id] = listener
