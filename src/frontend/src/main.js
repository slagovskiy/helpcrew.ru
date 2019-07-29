import Vue from 'vue'
import vuetify from './vuetify';

import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuelidate from 'vuelidate'
import VueLazyLoad from 'vue-lazyload'
import VueMoment from 'vue-moment'

import App from './App.vue'
import router from './router'
import store from './store'

import '@fortawesome/fontawesome-free/css/all.css'

//import config from './common/config'

Vue.use(Vuelidate)
Vue.use(VueAxios, axios)
Vue.use(VueLazyLoad)
Vue.use(VueMoment)

Vue.config.productionTip = false
//Vue.prototype.$config = config


new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
