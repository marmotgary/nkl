<template>
  <v-dialog v-model="dialog" persistent width="600px">
    <template v-slot:activator="{on}">
      <v-btn class="hidden-lg-and-up mb-5 ml-1" width="100%" v-on="on">Log In</v-btn>
      <v-btn class="hidden-md-and-down" v-on="on">Log in</v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Log In</span>
      </v-card-title>
      <v-card-text>
        <v-alert
          :value="alert"
          type="info"
          transition="scale-transition"
          outlined
        >Invalid user credentials.</v-alert>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex xs12>
              <v-text-field v-model="credentials.username" color="red darken-1" label="Email*" required></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                v-model="credentials.password"
                label="Password*"
                type="password"
                color="red darken-1"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions class=justify-center>
        <v-btn color="red darken-1" text @click="login">Log in</v-btn>
        <v-btn color="red darken-1" text @click="dialog = false, alert=false">Close</v-btn>
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
            this.$http
                .post('api/login/', this.credentials, {
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken')
                    },
                  'withCredentials': true,
                })
                .then(function(response) {
                    if (response.status === 200) {
                        this.dialog = !this.dialog;
                        this.alert = false;

                        localStorage.role_id = response.body.role;
                        localStorage.user_id = response.body.user.id;
                        localStorage.team_id = response.body.team_id
                        localStorage.player_name = response.body.user.player_name;

                        this.$session.set('role_id', response.body.role);
                        this.$session.set('user_id', response.body.user.id);
                        this.changeLogin(response.body.user.player_name);
                    }
                    },
                    response => {
                        this.alert = !this.alert;
                          if (response.status == 403) {
                            this.$http
                              .get('api/csrf/', {'withCredentials': true})
                              .then(function(response) {
                                  if (response.status === 200) {
                                    this.$http
                                        .post('api/login/', this.credentials, {
                                            headers: {
                                                'X-CSRFToken': this.getCookie('csrftoken')
                                            },
                                          'withCredentials': true,
                                        })
                                        .then(function(response) {
                                            if (response.status === 200) {
                                                this.dialog = !this.dialog;
                                                this.alert = false;

                                                localStorage.role_id = response.body.role;
                                                localStorage.user_id = response.body.user.id;
                                                localStorage.team_id = response.body.team_id
                                                localStorage.player_name = response.body.user.player_name;

                                                this.$session.set('role_id', response.body.role);
                                                this.$session.set('user_id', response.body.user.id);
                                                this.changeLogin(response.body.user.player_name);
                                            }
                                            },
                                            response => {
                                                this.alert = !this.alert;
                                            }).catch(function(response) {
                                                console.log(response);
                                          });
                                  }
                              });
  
                        }

                    }).catch(function(response) {
                        console.log(response);
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
