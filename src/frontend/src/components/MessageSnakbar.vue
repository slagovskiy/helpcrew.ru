<template>
    <div>
        <template v-if="error">
            <v-snackbar
                    v-bind:timeout="5000"
                    v-bind:multi-line="true"
                    color="error"
                    v-bind:value="errorShow"
            >{{error}}
                <v-icon v-on:click="hideError" color="white" style="cursor">fa-times-circle</v-icon>
            </v-snackbar>
        </template>
        <template v-if="message">
            <v-snackbar
                    v-bind:timeout="5000"
                    v-bind:multi-line="true"
                    color="primary"
                    v-bind:value="messageShow"
            >{{message}}
                <v-icon v-on:click="hideMessage" color="white" style="cursor">fa-times-circle</v-icon>
            </v-snackbar>
        </template>
    </div>
</template>

<script>
    import globalMixin from '../mixins/global'

    export default {
        mixins: [globalMixin,]
    }
</script>

<style scoped>

</style>