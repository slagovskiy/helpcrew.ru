import Vue from 'vue'
import Vuex from 'vuex'
import Global from './Global'
import Menu from './Menu'
import User from './User'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        menu: Menu,
        user: User,
        global: Global,
    },
    state: {},
    getters: {},
    mutations: {},
    actions: {}
})