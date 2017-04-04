from json import JSONDecodeError

import requests
from octoclient import OctoClient

from octoprint_dashboard.model import Printer


class OctoprintService:
    @staticmethod
    def auth(apikey, url):
        try:
            OctoClient(url=url, apikey=apikey)
        except RuntimeError as e:
            return {'message': {"apikey": "Invalid apikey"}}
        except requests.ConnectionError:
            return {'message': {"ip": "Invalid ip address"}}
        except JSONDecodeError:
            return {'message': {"ip": "Invalid ip address"}}
        except requests.Timeout:
            return {'message': {"ip": "Invalid ip address"}}
        return None

    @staticmethod
    def get_connection(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.connection_info()
        # return requests.get('http://{0}/api/connection'.format(printer.ip), headers={
        #     'X-Api-Key': printer.apikey
        # })

    @staticmethod
    def send_file(printer: Printer, filename, contents, print: bool):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.upload((filename, contents), print=print)
        # return requests.post('http://{0}/api/files/local'.format(printer.ip),
        #                      files={'file': (file.filename, file.read(), 'application/octet-stream')},
        #                      headers={
        #                          'X-Api-Key': printer.apikey
        #                      })

    @staticmethod
    def send_file_print(printer: Printer, file):
        return requests.post('http://{0}/api/files/local'.format(printer.ip),
                             files={'file': (file.filename, file.read(), 'application/octet-stream')},
                             data={'select': "true", 'print': "true"}, headers={
                'X-Api-Key': printer.apikey
            })

    @staticmethod
    def get_printer_state(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        status = client.printer()
        if status["state"]["text"] == "Printing" or status["state"]["text"] == "Paused":
            job_info = client.job_info()
            status["job"] = job_info["job"]
            status["job"]["progress"] = job_info["progress"]
        return status
        # return requests.get('http://{0}/api/printer'.format(printer.ip), headers={
        #     'X-Api-Key': printer.apikey
        # })

    @staticmethod
    def get_printer_state_repeated(printer: Printer):
        try:
            response = OctoprintService.get_printer_state(printer)
            return response
        except requests.ConnectionError:
            response = OctoprintService.get_printer_state(printer)
            return response

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
    def get_job_info(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.job_info()

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
    def delete_file(printer: Printer, origin, filename):
        try:
            client = OctoClient(url=printer.url, apikey=printer.apikey)
            client.delete(origin + "/" + filename)
            return True
        except RuntimeError:
            return False

    @staticmethod
    def print(printer: Printer, origin, filename):
        try:
            client = OctoClient(url=printer.url, apikey=printer.apikey)
            client.select(location=origin + "/" + filename, print=True)
            return True
        except RuntimeError:
            return False

    @staticmethod
    def get_settings(printer: Printer):
        return requests.get('{0}/api/settings'.format(printer.url), timeout=2,
                            headers={
            'X-Api-Key': printer.apikey
        })

    @staticmethod
    def save_settings(printer: Printer, settings):
        return requests.post('{0}/api/settings'.format(printer.url),
                             timeout=4,
                             json=settings,
                             headers={
            'X-Api-Key': printer.apikey
        })
