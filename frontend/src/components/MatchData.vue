<template>
      <v-card>
        <h3 class="text-md-left headline">
          Runkosarja kenttä <span v-if="this.match_field">{{this.match_field}}</span><span v-else>TBD</span>
          <span style="float:right;">{{ this.match_time | moment('YYYY-MM-DD HH:MM') }}</span>
        </h3>
        <v-row>
          <v-container fill-height>
            <v-col justify="center" align="center" class="ml-5">
              <figure>
                <img src="../../public/kyykkalogo120px.png">
                <figcaption v-if="this.home_team.score_total">
                  <br>
                  <v-chip
                    :color="`${this.home_team.color} lighten-2`"
                  >{{this.home_team.score_total}}</v-chip>
                </figcaption>
              </figure>
            </v-col>
            <v-col justify="center" align="center">
              <a :href="'/joukkue/'+this.home_team.id">{{this.home_team.name}}</a>
            </v-col>
            <v-col justify="center" align="center">
              vs.
            </v-col>
            <v-col justify="center" align="center">
              <a :href="'/joukkue/'+this.away_team.id">{{this.away_team.name}}</a>
            </v-col>            
            <v-col justify="center" align="center" class="mr-5">
              <figure style="float:right;">
                <img src="../../public/kyykkalogo120px.png">
                <figcaption v-if="this.home_team.score_total">
                  <br>
                  <v-chip
                    :color="`${this.away_team.color} lighten-2`"
                  >{{this.away_team.score_total}}</v-chip>
                </figcaption>
              </figure>
            </v-col>
          </v-container>
        </v-row>
      </v-card>
</template>

<script>
export default {
    props: {
      matchData: Object,
    },
    data: function() {
        return {
            match_time: '',
            match_field: '',
            home_team: {
                name: '',
                score_total: '',
                color: ''
            },
            away_team: {
                name: '',
                score_total: '',
                color: ''
            }
        };
    },
    methods: {
        getMatch: function() {
          this.match_time = this.matchData.body.match_time;
          this.match_field = this.matchData.body.field;
          this.away_team.name = this.matchData.body.away_team.name;
          this.home_team.name = this.matchData.body.home_team.name;
          this.home_team.id = this.matchData.body.home_team.id;
          this.away_team.id = this.matchData.body.away_team.id;

          this.home_team.score_total = this.matchData.body.home_score_total;
          this.away_team.score_total = this.matchData.body.away_score_total;

          if (
              this.home_team.score_total > this.away_team.score_total
          ) {
              this.home_team.color = 'red';
              this.away_team.color = 'green';
          } else {
              this.home_team.color = 'green';
              this.away_team.color = 'red';
          }
        }
    },
    mounted: function() {
        this.getMatch();
    }
};
</script>

<style scoped>
a {
  color: black;
  text-decoration: none;
}


</style>
