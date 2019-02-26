<template>
  <v-layout>
    <v-flex xs7>
      <lorem-ipsum></lorem-ipsum>
    </v-flex>
    <v-flex xs5 class="right">
      <data-table></data-table>
    </v-flex>
  </v-layout>
</template>

<script>
import LoremIpsum from '@/components/LoremIpsum';
import DataTable from '@/components/DataTable';

export default {
    name: 'home',
    components: {
        LoremIpsum,
        DataTable
    }
};
</script>

<style scoped>
.right {
    padding-right: 3em;
    padding-top: 5em;
}
</style>
