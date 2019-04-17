<template>
  <v-layout>
    <v-flex xs9>
      <h1 class="topic">INFO</h1>
      <info></info>
    </v-flex>
    <v-flex xs3 class="right">
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
