/** @ngInject */
function GroupController($mdDialog, $document) {
  const $ctrl = this;

  this.showSettings = function ($event) {
    $mdDialog.show({
      template: '<group-settings group="$ctrl.group"></group-settings>',
      parent: angular.element($document.body),
      controller() {
        this.group = $ctrl.group;
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
    group: '='
  }
};
