/** @ngInject */
function Controller($mdDialog) {
  const $ctrl = this;
  this.presets = [];
  this.addPreset = function () {
    $ctrl.presets.push({name: $ctrl.newpreset, bed: 0, extruder: 0});
    $ctrl.newpreset = "";
  };

  this.removePreset = function (key) {
    $ctrl.presets.splice(key, 1);
  };

  this.submit = function () {
    if ($ctrl.temperatureForm.$valid) {
      $mdDialog.hide($ctrl.presets);
    }
  };

  this.cancel = function () {
    $mdDialog.cancel();
  };
}

export const printerSettings = {
  template: require('./printerSettings.html'),
  controller: Controller
};
