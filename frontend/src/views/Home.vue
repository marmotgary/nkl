<template>
  <v-layout>
    <v-flex xs10>
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
    name: 'home',
    components: {
        LoremIpsum,
        SideBar
    }
};
</script>

<style scoped>
.right {
    padding-right: 3em;
    padding-top: 6em;
}
</style>
