/** @ngInject */
function GroupController($mdDialog, $document) {
  const $ctrl = this;

  this.showSettings = function ($event) {
    $mdDialog.show({
      template: '<md-dialog flex="50" style="max-height: 90%"><group-settings group="$ctrl.group" printers="$ctrl.printers" layout="column"></group-settings></md-dialog>',
      parent: angular.element($document.body),
      controller() {
        this.group = $ctrl.group;
        this.printers = $ctrl.printers;
      },
      controllerAs: '$ctrl',
      targetEvent: $event,
      clickOutsideToClose: true,
      fullscreen: true,
      autoWrap: false
    });
  };
}

export const group = {
  template: require('./group.html'),
  controller: GroupController,
  bindings: {
    group: '=',
    printers: '='
  }
};
