<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm10 md8 lg6>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Change password</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form v-model="valid" ref="form" lazy-validation>
                            <v-text-field
                                    id="token" prepend-icon="fa-key" name="token" label="key from email" type="text"
                                    v-model="token"
                                    v-bind:rules="passwordRules"
                            ></v-text-field>
                            <v-text-field
                                    id="password" prepend-icon="fa-lock" name="password" label="New password" type="password"
                                    v-model="password"
                                    v-bind:counter="6"
                                    v-bind:rules="passwordRules"
                            ></v-text-field>
                            <v-text-field
                                    id="confirmPassword" prepend-icon="fa-lock" name="confirmPassword" label="Confirm New password" type="password"
                                    v-model="confirmPassword"
                                    v-bind:counter="6"
                                    v-bind:rules="confirmPasswordRules"
                            ></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary"
                               v-on:click.prevent="onSubmit"
                               v-bind:disabled="!valid"
                               v-bind:loading="loading"
                        >Change</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    // eslint-disable-next-line
    var reEmail = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

    export default {
        data() {
            return {
                valid: false,
                token: '',
                password: '',
                confirmPassword: '',
                passwordRules: [
                    v => !!v || 'Password is required',
                    v => (v && v.length >= 6) || 'Password must be equal or more than 6 characters'
                ],
                confirmPasswordRules: [
                    v => !!v || 'Password is required',
                    v => v === this.password || 'Password should match'
                ]
            }
        },
        mounted() {
            this.token = this.$route.query.t
        },
        computed: {
            loading() {
                return this.$store.getters.global
            },
            isAuthenticated() {
                return this.$store.getters.isAuthenticated
            }
        },
        methods: {
            onSubmit() {
                if (this.$refs.form.validate()) {
                    var data = {
                        'token': this.token,
                        'new_password': this.password
                    }
                    this.$store.dispatch('restorePassword2', data)
                        .then(() => {
                            this.$router.push({'name': 'user-login'})
                        })
                        .catch(() => {});
                    }
            },
        }
    }
</script>

<style scoped>

</style>
