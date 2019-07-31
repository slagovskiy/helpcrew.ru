<template>
    <v-app id="app">
        <v-navigation-drawer
                v-model="drawer"
                app
        >
            <v-list dense>
                <template
                        v-for="item in mainMenu"
                >
                    <template v-if="item.title.includes('---')">
                        <v-divider v-bind:key="item.title"></v-divider>
                    </template>
                    <template v-else>
                        <v-list-item
                                v-bind:key="item.title"
                                v-bind:to="item.link"
                                v-if="item.auth === isAuthenticated || item.auth == -1"
                        >
                            <v-list-item-action>
                                <v-icon>{{item.icon}}</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title>{{item.title}}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </template>
                </template>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar
                app
                color="primary"
                dark
        >
            <v-app-bar-nav-icon v-on:click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-img right src="@/assets/hc_logo_white.png" max-width="239"></v-img>
            <v-spacer></v-spacer>
            <v-toolbar-title v-if="user.email">
                <v-avatar size="36px" class="toolbar-avatar">
                    <img
                            v-if="user.avatar"
                            v-bind:src="user.url"
                            v-bind:alt="user.email"
                    >
                </v-avatar>
                {{user.email}}
            </v-toolbar-title>
            <v-toolbar-title v-else><v-icon left>fa-poo</v-icon>Guest</v-toolbar-title>
        </v-app-bar>

        <v-content>
            <v-container
                    fluid
                    fill-height
            >
                <v-layout>
                    <v-flex>
                        <app-message-snakbar></app-message-snakbar>
                        <router-view></router-view>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>
        <v-footer
                color="primary"
                app
        >
            <v-card
                    flat
                    tile
                    width="100%"
                    class="primary text-center"
            >
                <v-card-text class="white--text overline">
                    Helpcrew.ru &copy; 2018-{{ new Date().getFullYear() }} Sergey Lagovskiy
                </v-card-text>
            </v-card>
        </v-footer>
    </v-app>
</template>

<script>
    import userMixin from './mixins/user'
    import globalMixin from './mixins/global'
    import appMessageSnakbar from './components/MessageSnakbar.vue'

    export default {
        components: {
            appMessageSnakbar: appMessageSnakbar
        },
        mixins: [userMixin, globalMixin],
        data: () => ({
            drawer: null,
        }),
        computed: {
            mainMenu() {
                return this.$store.getters.mainMenu
            }
        }
    }
</script>

<style>
    .v-btn {
        padding-left: 15px !important;
        padding-right: 15px !important;
    }
    .cursor {
        cursor: pointer;
    }
</style>