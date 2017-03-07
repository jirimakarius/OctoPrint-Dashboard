/** @ngInject */
function Controller($mdDialog) {
  this.cancel = function () {
    $mdDialog.cancel();
  };
}

export const addPrinter = {
  template: require('./addPrinter.html'),
  controller: Controller
};
