<template>
  <v-layout row wrap align-center>
    <v-flex xm-12>
      <v-card>
        <v-flex px-2 mb-5>
          <h3 class="text-md-left headline">
            Runkosarja kenttä <span v-if="this.match_field">{{this.match_field}}</span><span v-else>TBD</span>
            <span style="float:right;">{{ this.match_time | moment('YYYY-MM-DD HH:MM') }}</span>
          </h3>
        </v-flex>
        <v-layout mx-5 pb-5 px-5 row wrap>
          <v-flex>
            <figure>
              <img src="../../public/kyykkalogo120px.png">
              <figcaption v-if="this.home_team.score_total">
                <br>
                <v-chip
                  style="margin-left:15%;"
                  :color="`${this.home_team.color} lighten-2`"
                >{{this.home_team.score_total}}</v-chip>
              </figcaption>
            </figure>
          </v-flex>
          <v-flex pt-5 text-xm-center class="justify-center align-center">
            <h2>
              <span class="third"><a :href="'/joukkue/'+this.home_team.id">{{this.home_team.name}}</a></span>
              <span class="third">vs.</span>
              <span class="third"><a :href="'/joukkue/'+this.away_team.id">{{this.away_team.name}}</a></span>
            </h2>
          </v-flex>
          <v-flex>
            <figure style="float:right;">
              <img src="../../public/kyykkalogo120px.png">
              <figcaption v-if="this.home_team.score_total">
                <br>
                <v-chip
                  style="margin-left:30%;"
                  :color="`${this.away_team.color} lighten-2`"
                >{{this.away_team.score_total}}</v-chip>
              </figcaption>
            </figure>
          </v-flex>
        </v-layout>
      </v-card>
    </v-flex>
  </v-layout>
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

          if(!this.matchData.body.is_validated) {
            this.home_team.score_total = '0'
            this.away_team.score_total = '0'
            this.home_team.color = 'red'
            this.away_team.color = 'red'
            return
          }

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
.third {
  float: left;
  width: 33%;
  text-align: center;
}

a {
  color: black;
  text-decoration: none;
}
</style>
