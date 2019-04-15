<template>
  <v-layout class="pt-5">
    <v-flex xs9>
      <pelaajat></pelaajat>
    </v-flex>
    <v-flex xs3 class="pl-3">
      <side-bar></side-bar>
    </v-flex>
  </v-layout>
</template>

<script>
import SideBar from '@/components/SideBar';
import Pelaajat from '@/components/Pelaajat';

export default {
    name: 'home',
    components: {
        Pelaajat,
        SideBar
    }
};
</script>

<style scoped>
</style>
