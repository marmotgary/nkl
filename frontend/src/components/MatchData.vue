<template>
  <v-layout row wrap align-center>
    <v-flex xm-12>
      <v-card>
        <v-flex px-2 mb-5>
          <h3 class="text-md-left headline">
            Runkosarja kenttä 5
            <span
              style="float:right;"
            >{{ this.match_time | moment('YYYY-MM-DD HH:MM') }}</span>
          </h3>
        </v-flex>
        <v-layout mx-5 pb-5 px-5 row wrap>
          <v-flex>
            <img src="../../public/kyykkalogo120px.png">
          </v-flex>
          <v-flex pt-5 text-xs-center class="justify-center align-center">
            <h1>{{this.home_team.name}} vs. {{this.away_team.name}}</h1>
            <h4>
              <v-chip :color="`${this.home_team.color} lighten-2`">{{this.home_team.score_total}}</v-chip>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
              <v-chip :color="`${this.away_team.color} lighten-2`">{{this.away_team.score_total}}</v-chip>
            </h4>
          </v-flex>
          <v-flex>
            <img style="float:right;" src="../../public/kyykkalogo120px.png">
          </v-flex>
        </v-layout>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
    data: function() {
        return {
            match_time: '',
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
            this.$http
                .get(
                    'https://kyykka.rauko.la/api/matches/' +
                        this.$route.fullPath.substr(
                            this.$route.fullPath.lastIndexOf('/') + 1
                        )
                )
                .then(function(response) {
                    console.log(response);
                    this.match_time = response.body.match_time;
                    this.away_team.name = response.body.away_team.name;
                    this.home_team.name = response.body.home_team.name;
                    this.home_team.score_total = response.body.home_score_total;
                    this.away_team.score_total = response.body.away_score_total;

                    if (
                        this.home_team.score_total > this.away_team.score_total
                    ) {
                        this.home_team.color = 'red';
                        this.away_team.color = 'green';
                    } else {
                        this.home_team.color = 'green';
                        this.away_team.color = 'red';
                    }
                });
        }
    },
    mounted: function() {
        this.getMatch();
    }
};
</script>

<style scoped>
</style>
