/** @ngInject */
function GroupController($mdDialog, $document, Group, $scope) {
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

  this.deleteGroup = function ($event) {
    const confirm = $mdDialog.confirm()
      .title('Delete chosen group?')
      .textContent(`Are you sure, you want to delete group ${$ctrl.group.name} ?`)
      .targetEvent($event)
      .ok('Of course, i\'m sure')
      .cancel('Nope, I changed my mind');
    $mdDialog.show(confirm)
      .then(() => {
        Group.deleteGroup($ctrl.group).then(() => {
          $scope.$parent.$ctrl.deleteGroup($ctrl.group);
        });
      }).catch(() => {});
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
