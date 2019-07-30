export default {
    methods: {
        closeMessages() {
            this.$store.dispatch('clearMessages')
        },
        hideMessage() {
            this.$store.dispatch('hideMessage')
        },
        hideError() {
            this.$store.dispatch('hideError')
        }
    },
    computed: {
        loading() {
            return this.$store.getters.loading
        },
        error() {
            return this.$store.getters.error
        },
        message() {
            return this.$store.getters.message
        },
        messageShow() {
            return this.$store.getters.messageShow
        },
        errorShow() {
            return this.$store.getters.errorShow
        }

    },
}
