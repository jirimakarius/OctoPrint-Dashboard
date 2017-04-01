from apscheduler.schedulers.background import BackgroundScheduler
from octoprint_dashboard.services import OctoprintService
from octoprint_dashboard.model import Printer, Config


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        printers = Printer.query.all()
        for printer in printers:
            Printer.states[printer.id] = {}
            self.add_printer_status_job(printer, Config.get_config().server_refresh)

    def add_printer_status_job(self, printer: Printer, seconds):
        self.scheduler.add_job(OctoprintService.inject_printer_state,
                               trigger='interval',
                               args=[printer],
                               id=str(printer.id),
                               seconds=seconds)

    def remove_printer_status_job(self, printer_ids):
        for printer in printer_ids:
            self.scheduler.remove_job(str(printer))