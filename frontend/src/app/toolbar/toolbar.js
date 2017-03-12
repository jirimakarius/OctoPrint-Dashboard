/* @ngInject */
function ToolbarController($auth, $state) {
  this.login = function () {
    // console.dir($auth);
    $auth.logout();
    // $auth.setToken("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzQ1Njc4OTAsIm5hbWUiOiJKb2huIERvZSJ9.kRkUHzvZMWXjgB4zkO3d6P1imkdp0ogebLuxnTCiYUU");
    // $log.log($auth.isAuthenticated());
    // console.dir($auth.getToken());
    // console.dir($auth.getPayload());
    $auth.authenticate('CVUT').then(response => {
      console.dir(response);
      // $log.log($auth.isAuthenticated());
      // console.dir($auth.getToken());
      // console.dir($auth.getPayload());
    }).catch(response => {
      console.dir(response);
    });
  };
  this.logout = function () {
    $auth.logout();
    $state.reload();
  };
  this.isAuthenticated = function () {
    return $auth.isAuthenticated();
  };
}

export const toolbar = {
  template: require('./toolbar.html'),
  controller: ToolbarController
  // controller: ['$auth',ToolbarController]
};
