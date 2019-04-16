<template>
  <v-layout class="pt-5">
    <v-flex xs8>
      <ottelu></ottelu>
    </v-flex>
  </v-layout>
</template>

<script>
import Ottelu from '@/components/SingleOttelu';

export default {
    name: 'SingleOtteluView',
    components: {
        Ottelu
    }
};
</script>

<style>
</style>
