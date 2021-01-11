<template>
  <v-layout>
    <v-row align="center" justify="center">
      <h1><a class="rules__link" href="/static/saannot.pdf" download="saannot.pdf">NKL Säännöt (pdf)</a></h1>
    </v-row>
  </v-layout>
</template>

<style>
.rules__link {
  text-decoration: none;
  color: red !important;
}

</style>

<script>
export default {
    name: 'info-view',
};
</script>