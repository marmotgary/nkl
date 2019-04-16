<template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <v-flex xs6>
        <v-card color="secondary">
          <round roundNumber="1" teamSide="home"></round>
        </v-card>
      </v-flex>
      <v-spacer></v-spacer>
      <v-flex xs6>
        <v-card color="secondary">
          <round roundNumber="1" teamSide="away"></round>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row wrap>
      <v-flex xs6>
        <v-card color="secondary">
          <round roundNumber="2" teamSide="home"></round>
        </v-card>
      </v-flex>
      <v-flex xs6>
        <v-card color="secondary">
          <round roundNumber="2" teamSide="away"></round>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Round from '@/components/SingleRound';

export default {
    name: 'ottelu',
    components: {
        Round
    }
};
</script>
