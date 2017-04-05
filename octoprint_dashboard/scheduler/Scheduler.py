from apscheduler.schedulers.background import BackgroundScheduler
from octoprint_dashboard.services import OctoprintService
from octoprint_dashboard.model import Printer, Config


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.start()
        printers = Printer.query.all()
        config = Config.query.first()
        for printer in printers:
            Printer.states[printer.id] = {}
            self.add_printer_status_job(printer, config.server_refresh)

    def add_printer_status_job(self, printer: Printer, seconds):
        self.scheduler.add_job(OctoprintService.inject_printer_state,
                               trigger='interval',
                               args=[printer],
                               id=str(printer.id),
                               seconds=seconds)

    def remove_printer_status_job(self, printer_ids):
        for printer in printer_ids:
            self.scheduler.remove_job(str(printer))

    def reschedule(self, seconds):
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            job.reschedule(trigger='interval', seconds=seconds)
