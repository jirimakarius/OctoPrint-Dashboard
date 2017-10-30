export default angular.module('authServices', [])
/** @ngInject */
    .factory('auth', ($auth, $rootScope) => {
      function oauth() {
        return $rootScope.configPromise.then(() => {
          return $rootScope.auth !== "none";
        });
      }

      function isAuthenticated() {
        return oauth().then(auth => {
          if (auth) {
            return $auth.isAuthenticated();
          }
          return true;
        });
      }
      function logout() {
        return oauth().then(auth => {
          if (auth) {
            return $auth.logout();
          }
          return true;
        });
      }
      function authenticate(str) {
        return oauth().then(auth => {
          if (auth) {
            return $auth.authenticate(str);
          }
          return true;
        });
      }
      function setToken(token) {
        return oauth().then(auth => {
          if (auth) {
            return $auth.setToken(token);
          }
          return true;
        });
      }
      function getPayload() {
        return oauth().then(auth => {
          if (auth) {
            return $auth.setToken();
          }
          return {username: "Human", role: "Superhero"};
        });
      }
      function getToken() {
        if ($rootScope.auth === "none") {
          return "IShallPass";
        }
        return $auth.getToken();
      }
      function isRole(role) {
        return oauth().then(auth => {
          if (auth) {
            return $auth.getPayload().role === role;
          }
          return true;
        });
      }
      return {
        oauth, isAuthenticated, logout, authenticate, setToken, getPayload, getToken, isRole
      };
    });
