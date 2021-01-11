<template>
  <v-app class="app">
    <nav-bar class="mb-5"></nav-bar>
    <v-main transition="slide-x-transition" class="content pa-0 mx-auto">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import NavBar from '@/components/NavBar';

sessionStorage.season_id = '2';

export default {
    name: 'App',
    components: {
        NavBar
    }
};
</script>

<style scoped>
.content {
    width: 90%;
}

.app {
    background-color: transparent;
    overflow: hidden;
}
</style>
