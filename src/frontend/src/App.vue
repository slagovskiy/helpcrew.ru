<template>
    <v-app id="app">
        <v-navigation-drawer
                v-model="drawer"
                app
        >
            <v-list dense>
                <v-list-item>
                    <v-list-item-action>
                        <v-icon>fa-home</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Home</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-action>
                        <v-icon>fa-user</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Contact</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar
                app
                color="primary"
                dark
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>Help crew</v-toolbar-title>
        </v-app-bar>

        <v-content>
            <v-container
                    fluid
                    fill-height
            >
                <v-layout
                        align-center
                        justify-center
                >
                    <v-flex>
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
    export default {
        props: {
            source: String,
        },
        data: () => ({
            drawer: null,
        }),
    }
</script>