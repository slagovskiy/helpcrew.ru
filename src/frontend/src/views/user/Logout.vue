<template>
    <div></div>
</template>

<script>
    export default {
        created() {
            this.$store.dispatch('logout')
                .then(() => {
                    this.$router.push('/')
                })
                .catch(() => {
                })
        }
    }
</script>

<style scoped>

</style>