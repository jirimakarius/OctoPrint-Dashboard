export default eventListeners;

/** @ngInject */
function eventListeners($transitions) {
  $transitions.onStart({to: state => angular.isDefined(state.data) && state.data.security === true}, trans => {
    const $auth = trans.injector().get('$auth');

    if (!$auth.isAuthenticated()) {
      return trans.router.stateService.target('main');
    }
  });
}
