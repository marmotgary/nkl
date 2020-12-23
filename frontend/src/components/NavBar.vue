<template>
  <span>
    <v-flex mt-10></v-flex>
    <v-app-bar color="grey darken-2" dark>
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
      <div class="hidden-sm-and-down" v-if="!loggedIn">
        <log-in></log-in>
        <register></register>
      </div>
      <div v-if="loggedIn">
        {{ name }}
        <v-btn text class="hidden-sm-and-down" v-on:click.native="logout()" :to="'/'">Kirjaudu ulos</v-btn>
      </div>
      <v-spacer></v-spacer>
      <v-app-bar-nav-icon class="hidden-md-and-up" @click.stop="drawer = !drawer"/>
    </v-app-bar>
    
      <v-navigation-drawer
      v-model="drawer"
      right
      absolute
      temporary
      >
      <v-layout column fill-height>
        <v-list
          nav
          dense
        >
          <v-list-item-group
            v-model="group"
            active-class="text--accent-4"
          >
            <v-list-item to="/">
              <v-list-item-icon>
                <v-icon>mdi-home</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Home</v-list-item-title>
            </v-list-item>

            <v-list-item to="/ottelut">
              <v-list-item-icon>
                <v-icon>mdi-space-invaders</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Ottelut</v-list-item-title>
            </v-list-item>

            <v-list-item to="/joukkueet">
              <v-list-item-icon>
                <v-icon>mdi-emoticon-poop</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Joukkueet</v-list-item-title>
            </v-list-item>

            <v-list-item to="/pelaajat">
              <v-list-item-icon>
                <v-icon>mdi-account-group</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Pelaajat</v-list-item-title>
            </v-list-item>

            <v-list-item to="/info">
              <v-list-item-icon>
                <v-icon>mdi-information-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Info</v-list-item-title>
            </v-list-item>

          <v-list-item v-if="loggedIn && team_id" :to="'/joukkue/'+this.team_id">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Oma joukkue</v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <v-spacer></v-spacer>
          <log-in v-if="!loggedIn" class="hidden-sm-and-down"></log-in>
          <register v-if="!loggedIn" class="hidden-sm-and-down"></register>
          <p v-if="loggedIn">{{ name }}</p>
          <v-btn v-if="loggedIn" text class="hidden-sm-and-down" v-on:click.native="logout()" :to="'/'">Kirjaudu ulos</v-btn>
        </div>
      </v-layout>
      </v-navigation-drawer>

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
            group: false,
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
.v-app-bar--fixed {
    position: inherit;
}
</style>
