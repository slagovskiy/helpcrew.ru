<template>
    <div class="row window-height items-center">
        <div class="col"></div>
        <div class="col-lg-6 col-md-8 col-sm-10 col-xs-11">
            <q-form ref="form">
                <q-card>
                    <q-card-section class="bg-primary text-white">
                        <div class="text-h6"><q-icon name="fa fa-key" left />Login</div>
                    </q-card-section>
                    <q-separator />
                    <q-card-section>
                        <q-input
                                filled
                                v-model="email"
                                label="Email *"
                                lazy-rules
                                v-bind:rules="emailRules"
                        />

                        <q-input
                                filled
                                type="password"
                                v-model="password"
                                label="Your password *"
                                lazy-rules
                                v-bind:rules="passwordRules"
                        />

                    </q-card-section>

                    <q-card-actions>
                        <q-btn label="Forgot your password?" flat/>
                        <q-space/>
                        <q-btn label="Login" flat color="primary"/>
                    </q-card-actions>
                </q-card>
            </q-form>
        </div>
        <div class="col"></div>
    </div>
</template>

<script>
    // eslint-disable-next-line
    var reEmail = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

    export default {
        name: "Login",
        data() {
            return {
                valid: false,
                email: 'slagovskiy@gmail.com',
                password: '123qwe',
                emailRules: [
                    v => !!v || 'E-mail is required',
                    v => reEmail.test(v) || 'E-mail must be valid'
                ],
                passwordRules: [
                    v => !!v || 'Password is required',
                    v => (v && v.length >= 6) || 'Password must be equal or more than 6 characters'
                ]
            }
        },
        computed: {
            isAuthenticated(state) {
                return state.isAuthenticated
            },
            loading() {
                return this.$store.getters.loading
            }
        },
        methods: {
            onSubmit() {
                this.$refs.form.validate()
                    .then(success => {
                        if(success) {
                            var user = {
                                'email': this.email,
                                'password': this.password
                            }
                            this.$store.dispatch('login', user)
                                .then(() => {
                                    if (this.$store.getters.jwt) {
                                        this.$store.dispatch('autoLogin')
                                            .then(() => {
                                                if (this.$route.query['redirect'])
                                                    this.$router.push(this.$route.query['redirect'])
                                                else
                                                    this.$router.push({name: 'user-profile'})
                                            })
                                    }
                                })
                                .catch(() => {
                                });
                        }
                    })
            },
            restorePassword() {
                this.$router.push({name: 'user-restore'});
            }
        }
    }
</script>

<style scoped>

</style>