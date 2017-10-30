export default eventListeners;

/** @ngInject */
function eventListeners($transitions, $rootScope, Config, SatellizerConfig) {
  $rootScope.configPromise = Config.getClientConfig()
        .then(response => {
          if (response.auth !== "none") {
            $transitions.onStart({to: state => angular.isDefined(state.data) && state.data.security === true}, trans => {
              const $auth = trans.injector().get('$auth');

              if (!$auth.isAuthenticated() || !$auth.getPayload().role) {
                return trans.router.stateService.target('main');
              }
            });
            SatellizerConfig.providers.CVUT.clientId = response.oauth_client_id;
            SatellizerConfig.providers.CVUT.redirectUri = response.oauth_redirect_uri;
          }
          $rootScope.auth = response.auth;
          $rootScope.config = response;
        });
}
