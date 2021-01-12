<template>
  <v-layout>
  <v-flex auto>
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