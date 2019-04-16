<template>
  <v-layout class="layout">
    <data-table></data-table>
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
</style>
