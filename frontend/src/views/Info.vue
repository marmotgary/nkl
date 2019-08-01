<template>
  <v-layout>
<<<<<<< HEAD
    <v-flex xs9>
=======
    <v-flex mt-3 xs8>
>>>>>>> 1a106a6c293f084244994738f8b1556f7fdbcbb5
      <h1 class="topic">Säännöt</h1>
      <info></info>
    </v-flex>
    <v-flex xs4 class="right">
      <side-bar></side-bar>
    </v-flex>
  </v-layout>
</template>

<script>
import Info from '@/components/Info';
import SideBar from '@/components/SideBar';

export default {
    name: 'info-view',
    components: {
        Info,
        SideBar
    }
};
</script>

<style>
.topic {
    padding-top: 1em;
}
</style>
