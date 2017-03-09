/** @ngInject */
function AdminController(Printer, Group, $mdDialog, $document) {
  this.addPrinter = function ($event) {
    $mdDialog.show({
      template: '<md-dialog><add-printer></add-printer></md-dialog>',
      parent: angular.element($document.body),
      targetEvent: $event,
      preserveScope: true,
      clickOutsideToClose: true,
      fullscreen: true,
      autoWrap: false
    });
  };

  this.addGroup = function ($event) {
    $mdDialog.show({
      template: '<md-dialog><add-group></add-group></md-dialog>',
      parent: angular.element($document.body),
      targetEvent: $event,
      preserveScope: true,
      clickOutsideToClose: true,
      fullscreen: true
    });
  };

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
