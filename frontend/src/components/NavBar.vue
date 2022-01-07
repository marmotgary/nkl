<template>
  <span>
    <v-flex mt-10></v-flex>
    <v-app-bar style="z-index:2;" color="grey darken-3" dark>
      <router-link
        to="/"
        style="text-decoration: none; color:white; padding-right:2em; padding-left:1em;"
      >
        <img src="../../public/kyykkalogo120px.png">
      </router-link>
      <v-btn text class="hidden-md-and-down" to="/ottelut">Ottelut</v-btn>
      <v-btn text class="hidden-md-and-down" to="/joukkueet">Joukkueet</v-btn>
      <v-btn text class="hidden-md-and-down" to="/pelaajat">Pelaajat</v-btn>
      <v-btn
        v-if="loggedIn && team_id != 'null' && team_id"
        text
        class="hidden-md-and-down"
        :to="'/joukkue/'+this.team_id"
      >oma joukkue</v-btn>
      <v-btn text class="hidden-md-and-down" to="/info">Info</v-btn>
      <v-spacer class="hidden-md-and-down"></v-spacer>
      <v-spacer class="hidden-md-and-down"></v-spacer>
      <v-select v-on:input="selectSeason(items.name)" item-color=red v-model="selectedSeason" class="mt-4" align:center item-text="name" :items="seasons"></v-select>
      <v-spacer class="hidden-md-and-down"></v-spacer>
      <v-spacer class="hidden-md-and-down"></v-spacer>
      <div class="hidden-md-and-down pa-4" v-if="!loggedIn">
        <log-in></log-in>
      </div>
      <div class="hidden-md-and-down" v-if="!loggedIn">
        <register></register>
      </div>
      <div class="hidden-md-and-down" v-if="loggedIn">
        <span class="mr-5">{{ name }}</span>
        <v-btn class="hidden-md-and-down" v-on:click.native="logout()" :to="'/'">Kirjaudu ulos</v-btn>
      </div>
      <v-spacer></v-spacer>
      <v-app-bar-nav-icon class="hidden-lg-and-up mr-4" @click.stop="drawer = !drawer"/>
    </v-app-bar>
      <v-navigation-drawer
      v-model="drawer"
      right
      absolute
      temporary
      dark
      >
        <v-list nav>
          <v-list-item-group
            active-class="text--accent-4"
          >
            <v-list-item to="/">
              <v-list-item-icon>
                <v-icon>mdi-home</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Koti</v-list-item-title>
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

            <v-list-item v-if="loggedIn && team_id" :to="'/joukkue/'+this.team_id">
              <v-list-item-icon>
                <v-icon>mdi-account</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Oma joukkue</v-list-item-title>
            </v-list-item>

            <v-list-item to="/info">
              <v-list-item-icon>
                <v-icon>mdi-information-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Info</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <div class="pa-2">
                <log-in v-if="!loggedIn"></log-in>
                <register v-if="!loggedIn"></register>
              </div>
              <v-btn style="position:absolute;" width="95%" v-if="loggedIn" v-on:click.native="logout()" :to="'/'">Log out</v-btn>
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <template v-if="loggedIn" v-slot:prepend>
          <v-list-item two-line>
            <v-list-item-avatar>
              <img src="https://www.robertharding.com/watermark.php?type=preview&im=RF/RH_RF/VERTICAL/1112-5071">
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{ name }}</v-list-item-title>
              <v-list-item-subtitle>Logged In</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </template>
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
            name: '',
            team_id: '',
            selectedSeason: {
              value: '3'
            },
            items: [
                { title: 'Ottelut' },
                { title: 'Joukkueet' },
                { title: 'Pelaajat' },
                { title: 'Info' }
            ],
            seasons: [
              { name: 'Kausi 2020', value: '1', id: 1},
              { name: 'Kausi 2021', value: '2', id: 2},
              { name: 'Kausi 2022', value: '3', id: 3},
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
        },
        selectSeason () {
          sessionStorage.season_id = this.selectedSeason;
          this.$router.push('/').catch(()=>{
            window.location.reload();
          });;
        }
    },
    created() {
        if (sessionStorage.season_id) {
          this.selectedSeason = sessionStorage.season_id;
        }

        eventBus.$on('loginChanged', data => {
            this.loggedIn = true;
            this.name = data;

            if (localStorage.team_id != 'null' && localStorage.team_id) {
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

.v-data-table-header th {
  white-space: nowrap;
}
</style>


<style scoped>
.v-app-bar--fixed {
    position: inherit;
}

.v-select {
  width: 7%;
}
</style>
