import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap/dist/css/bootstrap.css'
import App from './App.vue'
import Vue from 'vue'
import VueAxios from 'vue-axios'
import axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import * as VueCookie from 'vue-cookie'
import FlashMessage from '@smartweb/vue-flash-message';



Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')

// Install BootstrapVue
Vue.use(BootstrapVue)

// Install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(VueAxios, axios)

Vue.use(VueCookie)

Vue.use(FlashMessage);