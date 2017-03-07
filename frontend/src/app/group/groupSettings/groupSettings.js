/** @ngInject */
function GroupSettingsController($mdDialog) {
  this.cancel = function () {
    $mdDialog.cancel();
  };
}

export const groupSettings = {
  template: require('./groupSettings.html'),
  controller: GroupSettingsController,
  bindings: {
    group: '='
  }
};
