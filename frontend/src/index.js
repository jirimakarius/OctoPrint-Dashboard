import angular from 'angular';

import {main} from './app/main/index';
import {toolbar} from './app/toolbar/toolbar';
import {printer} from './app/printer/printer';
import {control} from './app/control/control';
import {printerGrid} from './app/printerGrid/printerGrid';
import {admin} from './app/admin/admin';
import './app/services/restServices';
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
import eventListeners from './app/services/eventListeners';

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
  .component('admin', admin)
  .run(eventListeners);
