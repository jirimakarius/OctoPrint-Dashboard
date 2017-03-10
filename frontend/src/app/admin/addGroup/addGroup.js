/** @ngInject */
function Controller($mdDialog, Group) {
  const $ctrl = this;

  this.cancel = function () {
    $mdDialog.cancel();
  };

  this.submit = function () {
    Group.addGroup($ctrl.name)
      .then(() => {
        $mdDialog.hide();
      });
  };
}

export const addGroup = {
  template: require('./addGroup.html'),
  controller: Controller
};
