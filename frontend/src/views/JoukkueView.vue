<template>
  <v-layout>
    <v-flex auto >
      <joukkue></joukkue>
    </v-flex>
    <v-flex pl-2 class="hidden-md-and-down">
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
