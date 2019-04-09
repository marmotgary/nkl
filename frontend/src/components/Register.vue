<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <v-btn slot="activator">Register</v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">User Profile</span>
      </v-card-title>
      <v-card-text>
        <v-alert :value="alert" type="info" transition="scale-transition" outline>
          <b>Please correct the following error(s):</b>
          <ul>
            <li v-bind:key="error.id" v-for="error in errors">{{ error }}</li>
          </ul>
        </v-alert>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex xs12 sm6 md4>
              <v-text-field v-model="credentials.first_name" label="First name*" required></v-text-field>
            </v-flex>
            <v-flex xs12 sm6 md4>
              <v-text-field v-model="credentials.last_name" label="Last name*" required></v-text-field>
            </v-flex>
            <v-flex>
              <v-select v-model="credentials.number" :items="numbers"></v-select>
            </v-flex>
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
        <v-btn color="primary darken-1" flat @click="dialog = false">Close</v-btn>
        <v-btn color="primary darken-1" flat @click="register">Register</v-btn>
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
        numbers: [1, 2, 3]
    }),
    methods: {
        register() {
            this.$http.get('http://localhost:8000/api/csrf').then(response => {
                if (response.status === 200 && 'csrfToken' in response.body) {
                    this.$session.start();
                    this.$session.set('csrf', response.body.csrfToken);
                }
            });
            this.$http
                .post('http://localhost:8000/api/register/', this.credentials)
                .then(res => {
                    this.dialog = false;
                    this.alert = false;
                    this.changeLogin();
                })
                .catch(e => {
                    this.checkForm();
                });
        },
        checkForm: function(e) {
            this.errors = [];

            if (!this.alert) {
                this.alert = !this.alert;
            }

            if (!this.credentials.first_name) {
                this.errors.push('First name required.');
            }
            if (!this.credentials.last_name) {
                this.errors.push('Last name required.');
            }
            if (!this.credentials.username) {
                this.errors.push('Email required.');
            } else if (!this.validEmail(this.credentials.username)) {
                this.errors.push('Valid email required.');
            }
            if (!this.credentials.password) {
                this.errors.push('Password required.');
            }

            if (errors.length == 0) {
                changeLogin();
                return true;
            }
        },
        changeLogin: function() {
            eventBus.$emit(
                'loginChanged',
                this.credentials.first_name + ' ' + this.credentials.last_name
            );
        },
        validEmail: function(email) {
            var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }
    }
};
</script>

<style scoped>
</style>
