<template>
  <v-layout class="pt-5">
    <v-flex xs8>
      <ottelut></ottelut>
    </v-flex>
    <v-flex xs4 class="pl-3">
      <side-bar></side-bar>
    </v-flex>
  </v-layout>
</template>

<script>
import SideBar from '@/components/SideBar';
import Ottelut from '@/components/Ottelut';

export default {
    name: 'ottelutview',
    components: {
        SideBar,
        Ottelut
    }
};
</script>

<style>
</style>
