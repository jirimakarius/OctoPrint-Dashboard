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
    }).then(() => {
      Printer.getPrinters()
        .then(response => {
          $ctrl.printers = response;
        });
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
        Printer.removePrinters($ctrl.printers).then(() => {
          Printer.getPrinters()
            .then(response => {
              $ctrl.printers = response;
            });
        });
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
    }).then(() => {
      Group.getGroups()
        .then(response => {
          $ctrl.groups = response;
        });
    });
  };

  this.deleteGroup = function (group) {
    const index = $ctrl.groups.indexOf(group);
    console.dir(index);
    $ctrl.groups.splice(index, 1);
  };

  Printer.getPrinters()
    .then(response => {
      $ctrl.printers = response;
    });

  Group.getGroups()
    .then(response => {
      $ctrl.groups = response;
    });
}

export const admin = {
  template: require('./admin.html'),
  controller: AdminController
};
