<template>
    <q-layout view="lHh Lpr lFf">
        <q-header elevated class="">
            <q-toolbar>
                <q-btn
                        flat
                        dense
                        round
                        @click="leftDrawerOpen = !leftDrawerOpen"
                        aria-label="Menu"
                        icon="menu"
                />

                <q-toolbar-title>
                    Helpcrew
                </q-toolbar-title>

                <div>Quasar v{{ $q.version }}</div>
            </q-toolbar>
        </q-header>

        <q-drawer
                v-model="leftDrawerOpen"
                bordered
                content-class="bg-grey-2"
        >
            <q-list>
                <q-item-label header>Navigation</q-item-label>
                <q-item to="/" exact>
                    <q-item-section avatar>
                        <q-icon name="home" />
                    </q-item-section>
                    <q-item-section>
                        <q-item-label>Home</q-item-label>
                    </q-item-section>
                </q-item>
                <q-item to="/about" exact>
                    <q-item-section avatar>
                        <q-icon name="info"/>
                    </q-item-section>
                    <q-item-section>
                        <q-item-label>About</q-item-label>
                    </q-item-section>
                </q-item>
            </q-list>
        </q-drawer>

        <q-page-container>
            <router-view/>
        </q-page-container>
    </q-layout>
</template>

<script>
    export default {
        name: 'LayoutDefault',

        data() {
            return {
                leftDrawerOpen: this.$q.platform.is.desktop
            }
        }
    }
</script>
