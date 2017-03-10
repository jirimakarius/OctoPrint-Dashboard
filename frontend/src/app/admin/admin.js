/** @ngInject */
function AdminController(Printer, Group, $mdDialog, $document) {
  const $ctrl = this;

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

  this.removePrinters = function ($event) {
    const confirm = $mdDialog.confirm()
      .title('Delete chosen printers?')
      .textContent('Are you sure, you want to delete selected printers?')
      .targetEvent($event)
      .ok('Of course, i\'m sure')
      .cancel('Nope, I changed my mind');
    $mdDialog.show(confirm)
      .then(() => {
        Printer.removePrinters($ctrl.printers);
      }).catch(() => {});
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
      this.printers = response;
    });

  Group.getGroups()
    .then(response => {
      this.groups = response;
    });
}

export const admin = {
  template: require('./admin.html'),
  controller: AdminController
};
