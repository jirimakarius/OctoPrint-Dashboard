/** @ngInject */
function GroupController($mdDialog, $document) {
  const $ctrl = this;

  this.showSettings = function ($event) {
    $mdDialog.show({
      template: '<group-settings group="$ctrl.group" printers="$ctrl.printers"></group-settings>',
      parent: angular.element($document.body),
      controller() {
        this.group = $ctrl.group;
        this.printers = $ctrl.printers;
      },
      controllerAs: '$ctrl',
      targetEvent: $event,
      clickOutsideToClose: true,
      fullscreen: true
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
