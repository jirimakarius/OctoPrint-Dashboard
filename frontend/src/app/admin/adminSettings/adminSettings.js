/** @ngInject */
function Controller(Config) {
  const $ctrl = this;

  Config.getConfig()
    .then(response => {
      $ctrl.config = response;
    });
}

export const adminSettings = {
  template: require('./adminSettings.html'),
  controller: Controller
};
