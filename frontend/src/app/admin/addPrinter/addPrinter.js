/** @ngInject */
function Controller($mdDialog, Printer) {
  const $ctrl = this;

  this.cancel = function () {
    $mdDialog.cancel();
  };

  this.submit = function () {
    Printer.addPrinter({name: $ctrl.name, apikey: $ctrl.apikey, ip: $ctrl.ip})
      .then(() => {
        $mdDialog.hide();
      });
  };
}

export const addPrinter = {
  template: require('./addPrinter.html'),
  controller: Controller
};
