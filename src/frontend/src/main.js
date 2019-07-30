import Vue from 'vue'
import vuetify from './vuetify';

import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuelidate from 'vuelidate'
import VueLazyLoad from 'vue-lazyload'
import VueMoment from 'vue-moment'

import App from './App.vue'
import router from './router'
import store from './store/index'

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
    render: h => h(App),
    created() {
        router.beforeEach((to, from, next) => {
            if (to.matched.some(record => record.meta.requiresAuth)) {
                if (!this.$store.getters.isAuthenticated) {
                    next({
                        path: this.$router.resolve({name: 'user-login'}).href,
                        query: {redirect: to.fullPath}
                    })
                } else {
                    next()
                }
            } else {
                next()
            }
        })

        this.$store.dispatch('autoLogin')
    }
}).$mount('#app')
