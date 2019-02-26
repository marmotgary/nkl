<template>
  <v-app>
    <carousel></carousel>
    <nav-bar></nav-bar>
    <v-content transition="slide-x-transition">
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import Carousel from '@/components/Carousel';
import NavBar from '@/components/NavBar';

export default {
    name: 'App',
    components: {
        Carousel,
        NavBar
    }
};
</script>

<style scoped>
v-content {
    padding-top: 0;
}
</style>
