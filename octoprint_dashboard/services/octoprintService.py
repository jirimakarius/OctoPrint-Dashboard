import requests
from octoprint_dashboard.model import Printer
from octoclient import OctoClient
import random


class OctoprintService:
    @staticmethod
    def auth(apikey, url):
        try:
            OctoClient(url=url, apikey=apikey)
        except RuntimeError as e:
            return e.args[0]
        except requests.ConnectionError:
            return "Invalid ip address"
        return None

    @staticmethod
    def get_connection(printer: Printer):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.connection_info()
        # return requests.get('http://{0}/api/connection'.format(printer.ip), headers={
        #     'X-Api-Key': printer.apikey
        # })

    @staticmethod
    def send_file(printer: Printer, file, print: bool):
        client = OctoClient(url=printer.url, apikey=printer.apikey)
        return client.upload((file.filename, file.read()), print=print)
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
        if status["state"]["text"]=="Printing":
            job_info = client.job_info()
            status["job"]=job_info["job"]
            status["progress"]= job_info["progress"]
        return status
        # return requests.get('http://{0}/api/printer'.format(printer.ip), headers={
        #     'X-Api-Key': printer.apikey
        # })

    @staticmethod
    def inject_printer_state(printer: Printer):
        try:
            response = OctoprintService.get_printer_state(printer)
            Printer.states[printer.id] = response
        except requests.ConnectionError:
            Printer.states[printer.id] = {"state": {"text": "Offline/Unreachable"}}
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