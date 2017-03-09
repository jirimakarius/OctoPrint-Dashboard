/** @ngInject */
function AdminController(Printer, Group, $mdDialog, $document) {
  this.addPrinter = function ($event) {
    $mdDialog.show({
      template: '<add-printer></add-printer>',
      parent: angular.element($document.body),
      targetEvent: $event,
      // scope: $scope,
      // preserveScope: true,
      clickOutsideToClose: true,
      fullscreen: true
    });
  };

  this.addGroup = function ($event) {
    $mdDialog.show({
      template: '<add-group></add-group>',
      parent: angular.element($document.body),
      targetEvent: $event,
      // scope: $scope,
      // preserveScope: true,
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
