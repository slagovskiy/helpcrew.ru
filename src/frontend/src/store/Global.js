export default {
    state: {
        loading: false,
        error: null,
        errorShow: false,
        message: null,
        messageShow: false
    },
    mutations: {
        setLoading(state, payload) {
            state.loading = payload
        },
        setError(state, payload) {
            state.error = payload
            state.errorShow = true
        },
        hideError(state) {
            state.errorShow = false
        },
        setMessage(state, payload) {
            state.message = payload
            state.messageShow = true
        },
        hideMessage(state) {
            state.messageShow = false
        },
        clearMessages(state) {
            state.message = null
            state.messageShow = false
            state.error = null
            state.errorShow = false
        },
    },
    actions: {
        setLoading({commit}, payload) {
            commit('setLoading', payload)
        },
        setError({commit}, payload) {
            commit('setError', payload)
        },
        hideError({commit}) {
            commit('hideError')
        },
        setMessage({commit}, payload) {
            commit('setMessage', payload)
        },
        hideMessage({commit}) {
            commit('hideMessage')
        },
        clearMessages({commit}) {
            commit('clearMessages')
        },
    },
    getters: {
        loading(state) {
            return state.loading
        },
        error(state) {
            return state.error
        },
        errorShow(state) {
            return state.errorShow
        },
        message(state) {
            return state.message
        },
        messageShow(state) {
            return state.messageShow
        },
    }
}

