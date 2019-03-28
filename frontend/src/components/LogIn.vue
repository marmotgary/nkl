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
        changeLogin: function() {
            eventBus.$emit('loginChanged', 'This Is a PlaceHolder');
        },
        login() {
            this.$http
                .post('http://localhost:8000/api/login/', this.credentials)
                .then(
                    response => {
                        this.dialog = !this.dialog;
                        this.alert = false;
                        this.changeLogin();
                    },
                    response => {
                        this.alert = !this.alert;
                    }
                );
        }
    }
};
</script>

<style>
</style>
