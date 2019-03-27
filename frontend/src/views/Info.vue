<template>
  <v-layout>
    <v-flex xs10>
      <h1 class="topic">INFO</h1>
      <lorem-ipsum></lorem-ipsum>
    </v-flex>
    <v-flex xs5 class="right">
      <side-bar></side-bar>
    </v-flex>
  </v-layout>
</template>

<script>
import LoremIpsum from '@/components/LoremIpsum';
import SideBar from '@/components/SideBar';

export default {
    name: 'info',
    components: {
        LoremIpsum,
        SideBar
    }
};
</script>

<style scoped>
.topic {
    padding-top: 1em;
}
</style>
