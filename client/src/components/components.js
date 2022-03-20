import Vue from 'vue'
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
import { required, min, max, digits, email, length, numeric } from 'vee-validate/dist/rules';

// Vee-Validate config
extend('required', required)
extend('max', max)
extend('min', min)
extend('digits', digits)
extend('email', email)
extend('length', length)
extend('numeric', numeric)
Vue.component('validation-provider', ValidationProvider)
Vue.component('validation-observer', ValidationObserver)

import AppBar from './AppBar.vue'
import ComponentDialog from './ComponentDialog.vue'
import NavDrawer from './NavDrawer.vue'

Vue.component('app-bar', AppBar)
Vue.component('component-dialog', ComponentDialog)
Vue.component('nav-drawer', NavDrawer)