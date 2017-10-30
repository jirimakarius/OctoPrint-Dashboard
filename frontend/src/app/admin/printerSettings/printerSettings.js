/** @ngInject */
function Controller($mdDialog, Printer, auth) {
  const $ctrl = this;
  this.presets = [];
  this.addPreset = function () {
    $ctrl.presets.push({name: $ctrl.newpreset, bed: 0, extruder: 0});
    $ctrl.newpreset = "";
  };

  this.$onInit = function () {
    $ctrl.state = 2;
    Printer.getSettings($ctrl.printers)
      .then(settings => {
        $ctrl.settings = settings;
        if (settings.length === 1) {
          $ctrl.printer = settings[0];
        }
      });
    auth.isRole("superadmin").then(bool => {
      $ctrl.isSuperAdmin = bool;
    });
  };

  this.validate = function (printer) {
    $ctrl.printer.valid = "progress";
    Printer.updatePrinter(printer)
      .then(() => {
        $ctrl.printer.valid = "true";
      })
      .catch(() => {
        $ctrl.printer.valid = "false";
      });
  };

  this.removePreset = function (key) {
    $ctrl.presets.splice(key, 1);
  };

  this.submit = function () {
    Printer.saveSettings($ctrl.printers, {temperature: {profiles: $ctrl.presets}});
  };

  this.cancel = function () {
    $mdDialog.cancel();
  };
}

export const printerSettings = {
  template: require('./printerSettings.html'),
  controller: Controller,
  bindings: {
    printers: '='
  }
};
