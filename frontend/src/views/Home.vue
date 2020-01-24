<template>
  <v-layout>
    <v-flex mt-5 auto>
      <h1 class="topic">Nationaali Kyykkä Liiga</h1>
      <lorem-ipsum></lorem-ipsum>
    </v-flex>
    <v-flex xs4 class="right hidden-md-and-down">
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

<style>
.right {
    padding-right: 3em;
    padding-top: 6em;
}
.layout {
    margin-bottom: 1em;
}
</style>
