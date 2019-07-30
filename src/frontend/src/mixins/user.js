export default {
    computed: {
        isAuthenticated() {
            return this.$store.getters.isAuthenticated
        },
        user() {
            return this.$store.getters.user
        },
    },
}
