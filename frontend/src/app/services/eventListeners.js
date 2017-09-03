export default eventListeners;

/** @ngInject */
function eventListeners($transitions, $rootScope, Config, SatellizerConfig) {
  $rootScope.configPromise = Config.getClientConfig()
    .then(response => {
      $rootScope.config = response;
      SatellizerConfig.providers.CVUT.clientId = response.oauth_client_id;
      SatellizerConfig.providers.CVUT.redirectUri = response.oauth_redirect_uri;
    });
  $transitions.onStart({to: state => angular.isDefined(state.data) && state.data.security === true}, trans => {
    const $auth = trans.injector().get('$auth');

    if (!$auth.isAuthenticated() || !$auth.getPayload().role) {
      return trans.router.stateService.target('main');
    }
  });
}
