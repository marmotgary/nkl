<template>
    <span>
        <v-navigation-drawer
            app
            v-model="drawer"
            class="gray lighten-2"
            dark
            disable-resize-watcher
        >
            <v-list>
                <template v-for="(item, index) in items">
                    <v-list-tile :key="index">
                        <v-list-tile-content>
                            {{ item.title }}
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-divider :key="`divider-${index}`"></v-divider>
                </template>
                <log-in></log-in>
                <register></register>
            </v-list>
        </v-navigation-drawer>
        <v-toolbar app color="black darken-4" dark>
            <v-toolbar-side-icon
                class="hidden-md-and-up"
                @click="drawer = !drawer"
            ></v-toolbar-side-icon>
            <v-spacer class="hidden-md-and-up"></v-spacer>
            <v-toolbar-title>{{ appTitle }}</v-toolbar-title>
            <v-btn flat class="hidden-sm-and-down">Tulokset</v-btn>
            <v-btn flat class="hidden-sm-and-down">Ottelut</v-btn>
            <v-btn flat class="hidden-sm-and-down">Joukkueet</v-btn>
            <v-btn flat class="hidden-sm-and-down">Pelaajat</v-btn>
            <v-btn flat class="hidden-sm-and-down">Säännöt</v-btn>
            <v-btn flat class="hidden-sm-and-down">Info</v-btn>
            <v-spacer class="hidden-sm-and-down"></v-spacer>
            <log-in class="hidden-sm-and-down"></log-in>
            <register class="hidden-sm-and-down"></register>
        </v-toolbar>
    </span>
</template>

<script>
import LogIn from '@/components/LogIn';
import Register from '@/components/Register';

export default {
    name: 'NavBar',
    components: {
        LogIn,
        Register
    },
    data() {
        return {
            appTitle: 'NKL',
            drawer: false,
            items: [
                { title: 'Tulokset' },
                { title: 'Ottelut' },
                { title: 'Joukkueet' },
                { title: 'Pelaajat' },
                { title: 'Säännöt' },
                { title: 'Info' }
            ]
        };
    }
};
</script>

<style scoped>
</style>
