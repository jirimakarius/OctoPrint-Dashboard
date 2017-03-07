/** @ngInject */
function Controller($mdDialog) {
  this.cancel = function () {
    $mdDialog.cancel();
  };
}

export const addGroup = {
  template: require('./addGroup.html'),
  controller: Controller
};
