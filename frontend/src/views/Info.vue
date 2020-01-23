<template>
  <v-layout>
    <v-flex class="text-xs-center">
      <h1><a href="/static/saannot.pdf" download="saannot.pdf">NKL Säännöt (pdf)</a></h1>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
    name: 'info-view',
};
</script>

<style>
a {
  color: red;
  text-decoration: none;
  font-size: 130%;
}

</style>
