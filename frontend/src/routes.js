export default routesConfig;

/** @ngInject */
function routesConfig($stateProvider, $urlRouterProvider, $locationProvider, $authProvider) {
  $locationProvider.html5Mode(true).hashPrefix('!');
  $urlRouterProvider.otherwise('/');

  $stateProvider
    .state('main', {
      url: '/',
      template: '<main layout="column" flex></main>'
    });

  $authProvider.oauth2({
    name: 'CVUT',
    url: '/auth',
    clientId: 'fd19e88d-740e-4c82-822c-fff99ef0c4cb',
    redirectUri: 'http://localhost:3000',
    authorizationEndpoint: 'https://auth.fit.cvut.cz/oauth/authorize',
    scope: ['urn:zuul:oauth'],
    scopeDelimiter: ' ',
    requiredUrlParams: ['scope']
  });

  $authProvider.oauth2({
    name: 'test',
    url: '/',
    clientId: 'd6d2b510d18471d2e22aa202216e86c42beac80f9a6ac2da505dcb79c7b2fd99',
    redirectUri: 'http://147.32.113.72:3000',
    authorizationEndpoint: 'http://oauth-ng-server.herokuapp.com'
  });
}
