<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm10 md8 lg6>
                <v-card class="elevation-12">
                    <v-toolbar dark color="error">
                        <v-icon left>fa-exclamation-triangle</v-icon>
                        <v-toolbar-title>Access denied</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        You do not have access to this section or you are not authorized.
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="error" v-on:click="home">
                            <v-icon>fa-home</v-icon>
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    export default {
        methods: {
            home() {
                this.$router.push({name: 'home'})
            }
        }

    }
</script>

<style scoped>

</style>