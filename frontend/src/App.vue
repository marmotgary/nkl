<template>
  <v-app id="app">
    <nav-bar></nav-bar>
    <v-content transition="slide-x-transition" class="content pa-0 mx-auto">
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import NavBar from '@/components/NavBar';

export default {
    name: 'App',
    components: {
        NavBar
    }
};
</script>

<style scoped>
.content {
    width: 80%;
}

.app {
    background-color: transparent;
    overflow: hidden;
}
</style>
