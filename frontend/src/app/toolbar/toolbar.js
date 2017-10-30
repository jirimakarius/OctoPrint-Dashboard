/** @ngInject */
function ToolbarController(auth, $state, $rootScope) {
  const $ctrl = this;

  this.login = function () {
    auth.logout();
    auth.authenticate('CVUT').then(response => {
      auth.setToken(response.data);
      $state.reload();
    });
  };
  this.logout = function () {
    auth.logout();
    $state.reload();
  };

  this.theme = function () {
    $rootScope.theme = "default";
  };

  this.$onInit = function () {
    auth.oauth().then(val => {
      $ctrl.oauth = val;
    });
    auth.isAuthenticated().then(val => {
      $ctrl.isAuthenticated = val;
    });
    auth.getPayload().then(val => {
      if (val) {
        $ctrl.isAdmin = (val.role !== "user");
        $ctrl.username = val.username;
      } else {
        $ctrl.isAdmin = false;
        $ctrl.username = "";
      }
    });
  };

  // this.username = this.isAuthenticated() ? auth.getPayload().username : "";
}

export const toolbar = {
  template: require('./toolbar.html'),
  controller: ToolbarController
};
