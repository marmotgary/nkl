<template>
  <v-layout>
    <v-flex xs10></v-flex>
    <v-flex xs5 class="right">
      <data-table></data-table>
    </v-flex>
  </v-layout>
</template>

<script>
import DataTable from '@/components/DataTable';

export default {
    name: 'home',
    components: {
        DataTable
    }
};
</script>

<style scoped>
.right {
    padding-right: 3em;
    padding-top: 6em;
}
</style>
