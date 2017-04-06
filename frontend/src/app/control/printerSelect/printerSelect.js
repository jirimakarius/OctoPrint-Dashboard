/** @ngInject */
function Controller($mdDialog) {
  const $ctrl = this;

  this.cancel = function () {
    $mdDialog.cancel();
  };

  this.submit = function () {
    const result = [];

    angular.forEach($ctrl.selected, (value, key) => {
      if (value) {
        result.push(key);
      }
    });
    if (result.length) {
      $mdDialog.hide(result);
    } else {
      $mdDialog.cancel();
    }
  };
}

export const printerSelect = {
  template: require('./printerSelect.html'),
  controller: Controller,
  bindings: {
    printers: '=',
    filename: '@'
  }
};
