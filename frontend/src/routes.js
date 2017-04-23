export default routesConfig;

/** @ngInject */
function routesConfig($stateProvider, $urlRouterProvider, $locationProvider, $authProvider, $mdThemingProvider, ENV) {
  $locationProvider.html5Mode(true).hashPrefix('!');
  $urlRouterProvider.otherwise('/');

  $stateProvider
    .state('main', {
      url: '/',
      template: '<main layout="column" flex></main>'
    })
    .state('admin', {
      url: '/admin',
      template: '<admin layout="column" flex></admin>',
      data: {
        security: true
      }
    });

  $authProvider.oauth2({
    name: 'CVUT',
    url: `${ENV.api}/auth`,
    clientId: 'fd19e88d-740e-4c82-822c-fff99ef0c4cb',
    redirectUri: 'http://localhost:3000',
    authorizationEndpoint: 'https://auth.fit.cvut.cz/oauth/authorize',
    scope: ['urn:zuul:oauth'],
    scopeDelimiter: ' ',
    requiredUrlParams: ['scope']
  });

  $mdThemingProvider.theme('default')
  // .dark();
    .primaryPalette('green', {
      default: '800'
    })
    .accentPalette('blue')
    .warnPalette('red')
    .dark();
  // .backgroundPalette('deep-orange');
}
