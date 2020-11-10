<template>
  <span>
    <v-flex mt-10></v-flex>
    <v-toolbar color="grey darken-2" dark>
      <v-app-bar-nav-icon class="hidden-md-and-up" @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-spacer></v-spacer>
      <router-link
        to="/"
        style="text-decoration: none; color:white; padding-right:2em; padding-left:1em;"
      >
        <img src="../../public/kyykkalogo120px.png">
      </router-link>
      <v-btn text class="hidden-sm-and-down" to="/ottelut">Ottelut</v-btn>
      <v-btn text class="hidden-sm-and-down" to="/joukkueet">Joukkueet</v-btn>
      <v-btn text class="hidden-sm-and-down" to="/pelaajat">Pelaajat</v-btn>
      <v-btn text class="hidden-sm-and-down" to="/info">Info</v-btn>
      <v-btn
        v-if="loggedIn && team_id"
        text
        class="hidden-sm-and-down"
        :to="'/joukkue/'+this.team_id"
      >oma joukkue</v-btn>
      <v-spacer class="hidden-sm-and-down"></v-spacer>
      <div v-if="!loggedIn">
        <log-in class="hidden-sm-and-down"></log-in>
        <register class="hidden-sm-and-down"></register>
      </div>
      <div v-if="loggedIn">
        {{ name }}
        <v-btn text class="hidden-sm-and-down" v-on:click.native="logout()" :to="'/'">Kirjaudu ulos</v-btn>
      </div>

      <v-spacer></v-spacer>
    </v-toolbar>
  </span>
</template>

<script>
import LogIn from '@/components/LogIn';
import Register from '@/components/Register';
import { eventBus } from '../main';

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
            loggedIn: false,
            name: '',
            team_id: '',
            items: [
                { title: 'Ottelut' },
                { title: 'Joukkueet' },
                { title: 'Pelaajat' },
                { title: 'Info' }
            ]
        };
    },
    methods: {
        logout() {
            this.loggedIn = false;
            this.name = '';
            this.team_id = '';
            this.$session.destroy();
            localStorage.clear();
            this.$http.post('api/logout/', {}, {
              headers: {
                'X-CSRFToken': this.getCookie('csrftoken')
              },
              'withCredentials': true,
            })
        }
    },
    created() {
        eventBus.$on('loginChanged', data => {
            this.loggedIn = true;
            this.name = data;
            if (localStorage.team_id) {
              this.team_id = localStorage.team_id
            }
            else {
                this.$http
                    .get(
                        'api/players/' +
                            localStorage.user_id
                    )
                    .then(function(response) {
                      if (response.body.team) {
                        this.team_id = response.body.team.id;
                        localStorage.team_id = this.team_id;
                      } else {
                        this.team_id = '';
                      }
                    });
            }
        });
    }
};
</script>
<style>
a {
  color: red;
  text-decoration: none;
  font-size: 130%;
}

</style>


<style scoped>
.v-toolbar--fixed {
    position: inherit;
}
</style>
