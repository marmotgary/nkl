<template>
  <v-layout class="pt-5">
    <v-flex xs8>
      <joukkue></joukkue>
    </v-flex>
    <v-flex xs5 mt-4 pt-1 class="pl-3">
      <side-bar></side-bar>
    </v-flex>
  </v-layout>
</template>

<script>
import Joukkue from '@/components/Joukkue';
import SideBar from '@/components/SideBar';

export default {
    name: 'joukkueview',
    components: {
        Joukkue,
        SideBar
    }
};
</script>

<style scoped>
</style>
