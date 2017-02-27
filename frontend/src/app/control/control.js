/** @ngInject */
function ControlController() {
  this.$onInit = function () {
  };
}

export const control = {
  template: require('./control.html'),
  controller: ControlController,
  bindings: {
    printers: '='
  }
};
