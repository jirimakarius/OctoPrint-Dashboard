/** @ngInject */
function AdminController(Printer, Group) {
  this.printers = [];

  Printer.getPrinters()
    .then(response => {
      this.printers = response.data;
    });

  Group.getGroups()
    .then(response => {
      this.groups = response.data;
    });
}

export const admin = {
  template: require('./admin.html'),
  controller: AdminController
};
