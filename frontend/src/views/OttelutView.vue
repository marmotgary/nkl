<template>
  <v-layout class="pt-5">
    <v-flex xs10>
      <ottelut></ottelut>
    </v-flex>
    <v-flex xs5 class="pl-3">
      <data-table></data-table>
    </v-flex>
  </v-layout>
</template>

<script>
import DataTable from '@/components/DataTable';
import Ottelut from '@/components/Ottelut';

export default {
    name: 'ottelutview',
    components: {
        DataTable,
        Ottelut
    }
};
</script>

<style scoped>
</style>
