from json import JSONDecodeError

import requests
from octoclient import OctoClient

from octoprint_dashboard.model import Printer


class OctoprintService:
    @staticmethod
    def auth(apikey, url):
        try:
            OctoClient(url=url, apikey=apikey)
        except (RuntimeError, JSONDecodeError, requests.ConnectionError, requests.Timeout):
            return False
        return None

    @staticmethod
    def get_connection(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.connection_info()

    @staticmethod
    def send_file(printer: Printer, filename, contents, print: bool):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.upload((filename, contents), print=print)

    @staticmethod
    def get_printer_state(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        status = client.printer()
        if status["state"]["text"] == "Printing" or status["state"]["text"] == "Paused":
            job_info = client.job_info()
            status["job"] = job_info["job"]
            status["job"]["progress"] = job_info["progress"]
        return status

    @staticmethod
    def inject_printer_state(printer: Printer):
        try:
            response = OctoprintService.get_printer_state(printer)
            Printer.states[printer.id] = response
            Printer.states[printer.id]["failed"] = False
        except requests.ConnectionError:
            if Printer.states[printer.id].get("failed"):
                Printer.states[printer.id] = {"state": {"text": "Offline/Unreachable"}}
            Printer.states[printer.id]["failed"] = True
        except RuntimeError:
            Printer.states[printer.id] = {"state": {"text": "Offline"}}

    @staticmethod
    def set_tool_temperature(printer: Printer, temperature):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.tool_target(temperature)

    @staticmethod
    def set_bed_temperature(printer: Printer, temperature):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.bed_target(temperature)

    @staticmethod
    def pause(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.pause()

    @staticmethod
    def cancel(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.cancel()

    @staticmethod
    def get_files(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.files()

    @staticmethod
    def get_file(printer: Printer, origin, filename):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.files(origin + "/" + filename)

    @staticmethod
    def delete_file(printer: Printer, origin, filename):
        try:
            client = OctoClient(url=printer.url, apikey=printer.apikey)
            client.delete(origin + "/" + filename)
            return True
        except (RuntimeError, requests.ConnectionError):
            return False

    @staticmethod
    def print(printer: Printer, origin, filename):
        try:
            client = OctoClient(url=printer.url, apikey=printer.apikey)
            client.select(location=origin + "/" + filename, print=True)
            return True
        except (RuntimeError, requests.ConnectionError):
            return False

    @staticmethod
    def get_settings(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.settings()

    @staticmethod
    def save_settings(printer: Printer, settings):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.settings(settings)

    @staticmethod
    def get_file_contents(printer: Printer, origin, filename):
        file_info = OctoprintService.get_file(printer, origin, filename).json()

        response = requests.get(file_info["refs"]["download"],
                                timeout=4,
                                headers={
                                    'X-Api-Key': printer.apikey
                                })
        return response.content
