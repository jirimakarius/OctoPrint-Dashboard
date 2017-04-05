/** @ngInject */
function Controller(Config) {
  const $ctrl = this;

  Config.getConfig()
    .then(response => {
      $ctrl.config = response;
    });

  this.submit = () => {
    if ($ctrl.configForm.$valid) {
      Config.saveConfig($ctrl.config);
    }
  };
}

export const adminSettings = {
  template: require('./adminSettings.html'),
  controller: Controller
};
