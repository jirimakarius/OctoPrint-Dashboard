import angular from 'angular';

import {main} from './app/main/index';
import {toolbar} from './app/toolbar/toolbar';
import {printer} from './app/printer/printer';
import {control} from './app/control/control';
import {printerGrid} from './app/printerGrid/printerGrid';
import './app/restServices';
import 'angular-ui-router';
import 'angular-animate';
import 'angular-aria';
import 'angular-messages';
import 'angular-material';
import 'angular-material/angular-material.css';
import 'angular-resource';
import 'angular-sortable-view';
import 'satellizer';
import 'ng-file-upload';
import routesConfig from './routes';

import './index.css';

export const app = 'app';

angular
  .module(app, ['ui.router', 'ngMaterial', 'satellizer', 'ngResource', 'restServices', 'angular-sortable-view', 'ngFileUpload'])
  .config(routesConfig)
  .component('main', main)
  .component('toolbar', toolbar)
  .component('printer', printer)
  .component('control', control)
  .component('printerGrid', printerGrid)
  .run(['$transitions', $transitions => {
    $transitions.onStart({to: state => angular.isDefined(state.data) && state.data.security === true}, trans => {
      const $auth = trans.injector().get('$auth');

      if (!$auth.isAuthenticated()) {
        return trans.router.stateService.target('main');
      }
    });
  }]);
