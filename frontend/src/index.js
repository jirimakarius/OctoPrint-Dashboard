import angular from 'angular';

import {main} from './app/main/index';
import {sidebar} from './app/sidebar/sidebar';
import {toolbar} from './app/toolbar/toolbar';
import {printer} from './app/printer/printer';
import {control} from './app/control/control';
import './app/restServices';
import 'angular-ui-router';
import 'angular-animate';
import 'angular-aria';
import 'angular-messages';
import 'angular-material';
import 'angular-material/angular-material.css';
import 'angular-resource';
import 'satellizer';
import routesConfig from './routes';

import './index.css';

export const app = 'app';

angular
  .module(app, ['ui.router', 'ngMaterial', 'satellizer', 'ngResource', 'restServices'])
  .config(routesConfig)
  .component('main', main)
  .component('toolbar', toolbar)
  .component('sidebar', sidebar)
  .component('printer', printer)
  .component('control', control);
