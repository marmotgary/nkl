<template>
  <v-layout>
    <v-flex auto>
      <pelaajat></pelaajat>
    </v-flex>
    <v-flex xs4 class="pl-3 hidden-md-and-down">
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

<style>
</style>
