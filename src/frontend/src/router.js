import Vue from 'vue'
import Router from 'vue-router'
import DefaultLayout from './layouts/Default.vue'
import Home from './views/Home.vue'
import About from './views/About.vue'
import UserLogin from './views/user/Login'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            component: DefaultLayout,
            children: [
                {
                    path: '',
                    name: 'home',
                    component: Home
                },
                {
                    path: '/about',
                    name: 'about',
                    component: About
                },
                /*
                {
                    path: '/user/profile',
                    component: User,
                    name: 'user-profile',
                    meta: {requiresAuth: true}
                },*/
                {
                    path: '/user/login',
                    component: UserLogin,
                    name: 'user-login',
                    meta: {requiresNoAuth: true}
                },/*
                {
                    path: '/user/logout',
                    component: Logout,
                    name: 'user-logout',
                    meta: {requiresAuth: true}
                },
                {
                    path: '/user/register',
                    component: Register,
                    name: 'user-register',
                    meta: {requiresNoAuth: true}
                },
                {
                    path: '/user/password',
                    component: ChangePassword,
                    name: 'user-password',
                    meta: {requiresAuth: true}
                },
                {
                    path: '/user/restore',
                    component: RestorePassword,
                    name: 'user-restore',
                    meta: {requiresNoAuth: true}
                },*/
            ],
        },

    ],
    mode: 'history',
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        if (to.hash) {
            return {selector: to.hash}
        }
        return {
            x: 0,
            y: 0
        }
    }
})
