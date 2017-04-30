/** @ngInject */
function AdminController(Printer, Group, $mdDialog, $document, $auth) {
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
    })
      .catch(() => {});
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
      Group.getEditableGroups()
        .then(response => {
          $ctrl.groups = response;
        });
    }).catch(() => {});
  };

  this.deleteGroup = function (group) {
    const index = $ctrl.groups.indexOf(group);
    $ctrl.groups.splice(index, 1);
  };

  this.isSuperAdmin = function () {
    return $auth.getPayload().role === "superadmin";
  };

  this.addSuperAdmin = function ($event) {
    $mdDialog.show({
      template: '<md-dialog><add-super-admin></add-super-admin></md-dialog>',
      parent: angular.element($document.body),
      targetEvent: $event,
      preserveScope: true,
      clickOutsideToClose: true,
      fullscreen: true,
      autoWrap: false
    });
  };

  this.showSettings = function ($event) {
    $mdDialog.show({
      template: '<md-dialog flex="75" style="height: 90%"><printer-settings layout="column" printers="$ctrl.printers" flex></printer-settings></md-dialog>',
      parent: angular.element($document.body),
      targetEvent: $event,
      preserveScope: true,
      controller() {
        this.printers = $ctrl.printers;
      },
      controllerAs: '$ctrl',
      clickOutsideToClose: true,
      fullscreen: true,
      autoWrap: false
    })
      .then(() => {}).catch(() => {});
  };

  Printer.getPrinters()
    .then(response => {
      $ctrl.printers = response;
    });

  Group.getEditableGroups()
    .then(response => {
      $ctrl.groups = response;
    });
}

export const admin = {
  template: require('./admin.html'),
  controller: AdminController
};
