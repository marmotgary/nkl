<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <v-btn slot="activator">Log In</v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">Log In</span>
      </v-card-title>
      <v-card-text>
        <v-alert
          :value="alert"
          type="info"
          transition="scale-transition"
          outline
        >Invalid user credentials.</v-alert>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex xs12>
              <v-text-field v-model="credentials.username" label="Email*" required></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                v-model="credentials.password"
                label="Password*"
                type="password"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" flat @click="dialog = false, alert=false">Close</v-btn>
        <v-btn color="blue darken-1" v-on:keyup.enter="login" flat @click="login">Log in</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { eventBus } from '../main';

export default {
    name: 'LogIn',
    data: () => ({
        dialog: false,
        alert: false,
        valid: true,
        loading: false,
        credentials: {}
    }),
    methods: {
        changeLogin: function(username) {
            eventBus.$emit('loginChanged', username);
        },
        login: function() {
            this.$session.start();
            this.$http.get('https://kyykka.rauko.la/api/csrf', {'withCredentials': true})
            this.$http
                .post('https://kyykka.rauko.la/api/login/', this.credentials, {
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    },
                  'withCredentials': true,
                })
                .then(function(response) {
                    if (response.status === 200) {
                        this.dialog = !this.dialog;
                        this.alert = false;

                        localStorage.role_id = response.body.role;
                        localStorage.user_id = response.body.user.id;
                        localStorage.player_name = response.body.user.player_name;

                        this.$session.set('role_id', response.body.role);
                        this.$session.set('user_id', response.body.user.id);
                        this.changeLogin(response.body.user.player_name);
                    }
                    },
                    response => {
                        this.alert = !this.alert;
                    }).catch(function(response) {
                      if (response.status == 403) {
                        this.$http
                          .get('https://kyykka.rauko.la/api/csrf', {'withCredentials': true})
                          .then(function(response) {
                              if (response.status === 200) {
                                  this.$http.patch(post_url, post_data, {
                                  headers: {
                                    'X-CSRFToken': this.getCookie('csrftoken')
                                  },
                                  'withCredentials': true,
                                  })
                              }
                          });
                      }
                  });
        }
    },
    mounted() {
      if (localStorage.role_id && localStorage.user_id) {
        this.$session.set('role_id', localStorage.role_id);
        this.$session.set('user_id', localStorage.user_id);
        this.changeLogin(localStorage.player_name)
      }
      if (localStorage.csrfToken) {
        this.$session.set('csrf', localStorage.csrfToken);
      }

    }
};
</script>

<style>
</style>
