<template>
  <v-layout class="pt-5">
    <v-flex xs10>
      <pelaajat></pelaajat>
    </v-flex>
    <v-flex xs5 class="pl-3">
      <data-table></data-table>
    </v-flex>
  </v-layout>
</template>

<script>
import DataTable from '@/components/DataTable';
import Pelaajat from '@/components/Pelaajat';

export default {
    name: 'home',
    components: {
        Pelaajat,
        DataTable
    }
};
</script>

<style scoped>
</style>
