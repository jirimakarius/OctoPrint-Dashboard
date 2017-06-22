import requests
from octoclient import OctoClient

from octoprint_dashboard.model import Printer


class OctoprintService:
    """
    This class is meant to be whole static to simulate singleton

    It is collection of functions for communication with OctoPrint via REST API
    """

    @staticmethod
    def auth(apikey, url):
        """
        Tries to connect to printer and return None on success
        """
        try:
            OctoClient(url=url, apikey=apikey)
        except (RuntimeError, requests.RequestException, ValueError):
            return False
        return None

    @staticmethod
    def get_connection(printer: Printer):
        """
        Returns connection info about printer
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.connection_info()

    @staticmethod
    def send_file(printer: Printer, filename, contents, print: bool):
        """
        Uploads file to printer and issues print command if argument print is true
        Returns information about file from OctoPrint
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.upload((filename, contents), print=print)

    @staticmethod
    def get_printer_state(printer: Printer):
        """
        Returns information about current state of printer including job info if is OctoPrint printing or paused
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        status = client.printer()
        if status["state"]["text"] == "Printing" or status["state"]["text"] == "Paused":
            job_info = client.job_info()
            status["job"] = job_info["job"]
            status["job"]["progress"] = job_info["progress"]
        return status

    @staticmethod
    def inject_printer_state(printer: Printer):
        """
        Injects printer state data to Printer states class variable.
        """
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
        """
        Issues tool target temperature command to OctoPrint
        Returns response with 204/No Content
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.tool_target(temperature)

    @staticmethod
    def set_bed_temperature(printer: Printer, temperature):
        """
        Issues bed target temperature command to OctoPrint
        Returns response with 204/No Content
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.bed_target(temperature)

    @staticmethod
    def pause(printer: Printer):
        """
        Issues pause print command to OctoPrint
        Returns response with 204/No Content
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.pause()

    @staticmethod
    def cancel(printer: Printer):
        """
        Issues cancel print command to OctoPrint
        Returns response with 204/No Content
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.cancel()

    @staticmethod
    def get_files(printer: Printer):
        """
        Returns data about files currently present on printer
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.files()

    @staticmethod
    def get_file(printer: Printer, origin, filename):
        """
        Returns data about specific file on printer
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.files(origin + "/" + filename)

    @staticmethod
    def delete_file(printer: Printer, origin, filename):
        """
        Deletes file on printer
        Returns true if success else false
        """
        try:
            client = OctoClient(url=printer.url, apikey=printer.apikey)
            client.delete(origin + "/" + filename)
            return True
        except (RuntimeError, requests.ConnectionError):
            return False

    @staticmethod
    def print(printer: Printer, origin, filename):
        """
        Issues print command to OctoPrint on given file
        Returns true if success else false
        """
        try:
            client = OctoClient(url=printer.url, apikey=printer.apikey)
            client.select(location=origin + "/" + filename, print=True)
            return True
        except (RuntimeError, requests.ConnectionError):
            return False

    @staticmethod
    def get_settings(printer: Printer):
        """
        Returns OctoPrints settings
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.settings()

    @staticmethod
    def save_settings(printer: Printer, settings):
        """
        Overwrites given OctoPrint settings
        """
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.settings(settings)

    @staticmethod
    def get_file_contents(printer: Printer, origin, filename):
        """
        Returns file contents
        Gets file information and downloads it's contents
        """
        file_info = OctoprintService.get_file(printer, origin, filename)

        response = requests.get(file_info["refs"]["download"],
                                timeout=4,
                                headers={'X-Api-Key': printer.apikey})
        return response.content
