<template>
  <v-container grid-list-md>
    <v-layout row wrap align-center>
      <v-flex xm12>
        <match></match>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xm6>
        <v-card color="secondary">
          <round roundNumber="1" teamSide="home"></round>
        </v-card>
      </v-flex>
      <v-flex xm6>
        <v-card color="secondary">
          <round roundNumber="1" teamSide="away"></round>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xm6>
        <v-card color="secondary">
          <round roundNumber="2" teamSide="home"></round>
        </v-card>
      </v-flex>
      <v-flex xm6>
        <v-card color="secondary">
          <round roundNumber="2" teamSide="away"></round>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Round from '@/components/SingleRound';
import Match from '@/components/MatchData';

export default {
    name: 'ottelu',
    components: {
        Round,
        Match
    }
};
</script>

<style>
</style>
