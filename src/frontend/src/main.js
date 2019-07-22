import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index'
import './quasar'

Vue.config.productionTip = false

new Vue({
    router,
    store,
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
            } else if (to.matched.some(record => record.meta.requiresNoAuth)) {
                if (this.$store.getters.isAuthenticated) {
                    next({
                        path: this.$router.resolve({name: 'user-profile'}).href
                    })
                } else {
                    next()
                }
            } else {
                next()
            }
        })

        //this.$store.dispatch('autoLogin')
    },
    render: h => h(App)
}).$mount('#app')
