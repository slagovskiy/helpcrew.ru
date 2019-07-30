import router from '../router'

export default {
    state: {
        mainMenu: [
            {
                icon: 'fa-home',
                title: 'Home',
                link: router.resolve({name: 'home'}).href,
                auth: false
            },
            {
                title: '---0',
            },
            {
                icon: 'fa-sign-in-alt',
                title: 'Login',
                link: router.resolve({name: 'user-login'}).href,
                auth: false
            },
            {
                icon: 'fa-user',
                title: 'Registration',
                link: router.resolve({name: 'user-register'}).href,
                auth: false
            },
            {
                icon: 'fa-key',
                title: 'Profile',
                link: router.resolve({name: 'user-profile'}).href,
                auth: true
            },
            {
                icon: 'fa-key',
                title: 'Change password',
                link: router.resolve({name: 'user-password'}).href,
                auth: true
            },
            {
                icon: 'fa-sign-out-alt',
                title: 'Logout',
                link: router.resolve({name: 'user-logout'}).href,
                auth: true
            },
            {
                title: '---1',
            },
        ],
    },
    getters: {
        mainMenu(state) {
            return state.mainMenu
        },
    }
}
