<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{on}">
      <v-btn v-on="on">Register</v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Rekisteröityminen</span>
      </v-card-title>
      <v-card-text>
        <v-alert :value="alert" type="info" transition="scale-transition" outline>
          <b>Korjaa seuraava(t):</b>
          <ul>
            <li v-bind:key="error.id" v-for="error in errors">{{ error }}</li>
          </ul>
        </v-alert>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-layout row>
              <v-flex xs5 sm6 md4>
                <v-text-field info v-model="credentials.first_name" label="Etunimi*" required></v-text-field>
              </v-flex>
              <v-flex xs5 sm6 md4 mr-5>
                <v-text-field info v-model="credentials.last_name" label="Sukunimi*" required></v-text-field>
              </v-flex>
              <v-flex xs2 sm2 ml-5>
                <v-select info v-model="credentials.number" required :items="numbers"></v-select>
              </v-flex>
            </v-layout>
            <v-flex xs12>
              <v-text-field info v-model="credentials.username" label="sähköposti*" type="email" required></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                info
                v-model="credentials.password"
                label="salasana*"
                type="password"
                required
              ></v-text-field>
              <v-text-field
                info
                v-model="credentials.password_check"
                label="salasana varmistus*"
                type="password"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
        <small>*pakollinen kenttä</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="info darken-1" text @click="dialog = false">Sulje</v-btn>
        <v-btn color="info darken-1" text @click="checkForm">Valmis</v-btn>
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
        response_errors: [],
        credentials: {},
        numbers: []
    }),
    methods: {
        register() {
            this.$http.get('api/csrf', {'withCredentials': true});
            this.$http
                .post('api/register/', this.credentials, {
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
                    this.response_errors = response.body;
                    this.checkForm();
                    if (response.status == 403) {
                      this.$http
                        .get('api/csrf', {'withCredentials': true})
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
        checkForm: function() {
            this.errors = []

            if (!this.alert) {
                this.alert = !this.alert;
            }

            if (this.response_errors.username == 'This field must be unique.') {
              this.errors.push('Sähköposti on jo käytössä.')
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
                this.errors.push('Anna salasana mallia foo@bar.xyz.');
            }
            if (!this.credentials.password) {
                this.errors.push('Salasana puuttuu.');
            }
            if (!this.credentials.number && this.credentials.number != 0) {
              this.errors.push('Pelaajanumero puuttuu.');
            }

            if (this.credentials.password !== this.credentials.password_check) {
              this.errors.push('Salasanat eivät täsmää.')
            }

            if (this.errors.length == 0) {
                this.changeLogin();
                this.register();
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
