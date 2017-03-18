import requests
from octoprint_dashboard.model import Printer
import random


class OctoprintService:
    @staticmethod
    def get_version(apikey, ip):
        return requests.get('http://{0}/api/version'.format(ip), headers={
            'X-Api-Key': apikey
        })

    @staticmethod
    def get_connection(printer: Printer):
        return requests.get('http://{0}/api/connection'.format(printer.ip), headers={
            'X-Api-Key': printer.apikey
        })

    @staticmethod
    def send_file(printer: Printer, file):
        # 'http://{0}/api/files/local'.format(printer.ip)
        # , 'select': "true", 'print': "true"
        # 'https://private-b4bd6-octoprintdashboardapi.apiary-mock.com/upload'
        return requests.post('http://{0}/api/files/local'.format(printer.ip),
                             files={'file': (file.filename, file.read(), 'application/octet-stream')},
                             headers={
                                 'X-Api-Key': printer.apikey
                             })

    @staticmethod
    def send_file_print(printer: Printer, file):
        return requests.post('http://{0}/api/files/local'.format(printer.ip),
                             files={'file': (file.filename, file.read(), 'application/octet-stream')},
                             data={'select': "true", 'print': "true"}, headers={
                'X-Api-Key': printer.apikey
            })

    @staticmethod
    def get_printer_state(printer: Printer):
        return requests.get('http://{0}/api/printer'.format(printer.ip), headers={
            'X-Api-Key': printer.apikey
        })

    @staticmethod
    def inject_printer_state(printer: Printer):
        # response = OctoprintService.get_printer_state(printer)
        # Printer.states[printer.id] = response.json()
        Printer.states[printer.id] = {
            "temperature": {
                "tool": random.randint(0, 500),
                "bed": random.randint(0, 300)
            },
            "state": "Operational"
        }
        # print(printer.id)
