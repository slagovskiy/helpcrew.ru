import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            component: () => import('./views/Home'),
            name: 'home',
            meta: {requiresAuth: false}
        },
        {
            path: '/user/profile',
            component: () => import('./views/user/Profile'),
            name: 'user-profile',
            meta: {requiresAuth: true}
        },
        {
            path: '/user/login',
            component: () => import('./views/user/Login'),
            name: 'user-login',
            meta: {requiresAuth: false}
        },
        {
            path: '/user/logout',
            component: () => import('./views/user/Logout'),
            name: 'user-logout',
            meta: {requiresAuth: false}
        },
        {
            path: '/user/restore',
            component: () => import('./views/user/Restore'),
            name: 'user-restore',
            meta: {requiresAuth: false}
        },
        {
            path: '/user/register',
            component: () => import('./views/user/Register'),
            name: 'user-register',
            meta: {requiresAuth: false}
        },
        {
            path: '/user/password',
            component: () => import('./views/user/Password'),
            name: 'user-password',
            meta: {requiresAuth: true}
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
