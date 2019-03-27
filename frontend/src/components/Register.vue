<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <v-btn slot="activator">Register</v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">User Profile</span>
      </v-card-title>
      <v-card-text>
        <v-alert :value="alert" type="info" transition="scale-transition" outline>{{alertMessage}}</v-alert>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex xs12 sm6 md4>
              <v-text-field v-model="credentials.first_name" label="First name*" required></v-text-field>
            </v-flex>
            <v-flex xs12 sm6 md4>
              <v-text-field v-model="credentials.last_name" label="Last name*" required></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                v-model="credentials.username"
                label="Email*"
                type="email"
                :rules="rules.email"
                required
              ></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                v-model="credentials.password"
                label="Password*"
                type="password"
                :rules="rules.password"
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
var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
export default {
    name: 'Register',
    data: () => ({
        dialog: false,
        alert: false,
        credentials: {},
        // Diis aways
        rules: {
            email: [
                v => !!v || this.alertMessage('Email is required'),
                v => re.test(v) || 'Enter a valid email address'
            ],
            password: [
                v => !!v || 'Password is required',
                v =>
                    (v && v.length > 7) ||
                    'The password must be longer than 7 characters'
            ]
        }
    }),
    methods: {
        register() {
            this.$http
                .post('http://localhost:8000/api/register/', this.credentials)
                .then(res => {
                    this.dialog = false;
                });
        },
        // Chang messuga here
        changeMessage(message) {}
    }
};
</script>

<style scoped>
</style>
