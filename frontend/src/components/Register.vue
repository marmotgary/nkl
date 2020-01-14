<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <v-btn slot="activator">Register</v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">User Profile</span>
      </v-card-title>
      <v-card-text>
        <v-alert :value="alert" type="error" transition="scale-transition" outline>
          <b>Please correct the following error(s):</b>
          <ul>
            <li v-bind:key="error.id" v-for="error in errors">{{ error }}</li>
          </ul>
        </v-alert>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-layout row>
              <v-flex xs5 sm6 md4>
                <v-text-field v-model="credentials.first_name" label="First name*" required></v-text-field>
              </v-flex>
              <v-flex xs5 sm6 md4 mr-5>
                <v-text-field v-model="credentials.last_name" label="Last name*" required></v-text-field>
              </v-flex>
              <v-flex xs2 sm2 ml-5>
                <v-select v-model="credentials.number" required :items="numbers"></v-select>
              </v-flex>
            </v-layout>
            <v-flex xs12>
              <v-text-field v-model="credentials.username" label="Email*" type="email" required></v-text-field>
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
        <v-btn color="error darken-1" flat @click="dialog = false">Close</v-btn>
        <v-btn color="error darken-1" flat @click="register">Register</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { eventBus } from '../main';

export default {
    name: 'Register',
    data: () => ({
        dialog: false,
        alert: false,
        errors: [],
        credentials: {},
        numbers: []
    }),
    methods: {
        register() {
            this.$http.get('https://kyykka.rauko.la/api/csrf', {'withCredentials': true});
            this.$http
                .post('http://localhost:8000/api/register/', this.credentials, {
                  headers: {
                    'X-CSRFToken': this.getCookie('csrftoken')
                  },
                  'withCredentials': true,        
                  })
                .then(function(response) {
                    this.dialog = false;
                    this.alert = false;

                    localStorage.role_id = response.body.role;
                    localStorage.user_id = response.body.user.id;
                    localStorage.player_name = response.body.user.player_name;

                    this.changeLogin();
                })
                .catch(function(response) {
                    this.checkForm();
                    if (response.status == 403) {
                      this.$http
                        .get('http://localhost:8000/api/csrf', {'withCredentials': true})
                        .then(function(response) {
                            if (response.status === 200) {
                                this.$http.patch(post_url, post_data, {
                                headers: {
                                  'X-CSRFToken': this.getCookie('csrftoken')
                                },
                                  'withCredentials': true,
                                }).then(function(response) {
                                  localStorage.role_id = response.body.role;
                                  localStorage.user_id = response.body.user.id;
                                  localStorage.player_name = response.body.user.player_name;
                                })
                            }
                        });
                    }
                });
        },
        checkForm: function(e) {
            this.errors = [];

            if (!this.alert) {
                this.alert = !this.alert;
            }

            if (!this.credentials.first_name) {
                this.errors.push('Etunimi puuttuu.');
            }
            if (!this.credentials.last_name) {
                this.errors.push('Sukunimi puuttuu.');
            }
            if (!this.credentials.username) {
                this.errors.push('Email puuttuu.');
            } else if (!this.validEmail(this.credentials.username)) {
                this.errors.push('Anna oikea sähköpostiosoite.');
            }
            if (!this.credentials.password) {
                this.errors.push('Salasana puuttuu.');
            }
            if (!this.credentials.number) {
              this.errors.push('Pelaajanumero puuttuu.');
            }

            if (errors.length == 0) {
                changeLogin();
                return true;
            }
        },
        changeLogin: function(username) {
            eventBus.$emit(
                'loginChanged',
                this.credentials.first_name + ' ' + this.credentials.last_name
            );
        },
        validEmail: function(email) {
            var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }
    },
    mounted: function() {
        this.numbers = Array.from(Array(100).keys());
    }
};
</script>

<style scoped>
</style>
