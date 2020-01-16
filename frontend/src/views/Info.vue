<template>
  <v-layout>
    <v-flex xs9 class="text-xs-center">
      <h1 class="topic"><a href="/frontend/public/saannot.pdf" target="_blank">NKL Säännöt</a></h1>
    </v-flex>
    <v-flex xs4 class="right">
      <side-bar></side-bar>
    </v-flex>
  </v-layout>
</template>

<script>
import SideBar from '@/components/SideBar';

export default {
    name: 'info-view',
    components: {
        SideBar
    }
};
</script>

<style>
.topic {
    padding-top: 4em;
}
</style>
