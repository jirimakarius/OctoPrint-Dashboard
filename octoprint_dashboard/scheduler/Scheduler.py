from apscheduler.schedulers.background import BackgroundScheduler
from octoprint_dashboard.services import OctoprintService
from octoprint_dashboard.model import Printer


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        printers = Printer.query.all()
        for printer in printers:
            self.add_printer_status_job(printer, 5)

    def add_printer_status_job(self, printer: Printer, seconds):
        self.scheduler.add_job(OctoprintService.inject_printer_state,
                               trigger='interval',
                               args=[printer],
                               id=str(printer.id),
                               seconds=seconds)
