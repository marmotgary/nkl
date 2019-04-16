<template>
  <v-card>
    <v-card-title>Erä {{this.roundNumber}}</v-card-title>
    <v-layout row wrap>
      <v-card-text>
        <p class="text-xs-left" v-if="this.teamSide == 'home'">
          {{this.home_team}}
          <v-btn style="float:right;">52</v-btn>
        </p>
        <p class="text-xs-left" v-if="this.teamSide == 'away'">
          {{this.away_team}}
          <v-btn style="float:right;">52</v-btn>
        </p>
      </v-card-text>
    </v-layout>
    <v-data-table :headers="headers" :items="data" hide-actions>
      <template slot="no-data">
        <v-progress-linear slot="progress" indeterminate></v-progress-linear>
      </template>
      <template slot="headers" class="text-xs-center"></template>
      <template slot="items" slot-scope="props">
        <td v-if="props.item.player.id">{{props.item.player.id}}</td>
        <td v-if="props.item.player.player_name">{{props.item.player.player_name}}</td>
        <td v-if="props.item.score_first">{{props.item.score_first}}</td>
        <td v-if="props.item.score_second">{{props.item.score_second}}</td>
        <td v-if="props.item.score_third">{{props.item.score_third}}</td>
        <td v-if="props.item.score_fourth">{{props.item.score_fourth}}</td>
        <td v-if="props.item.score_fourth">{{props.item.score_total}}</td>
      </template>
      <template slot="headers" class="text-xs-center"></template>
      <template></template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
    name: 'match-round',
    props: {
        roundNumber: String,
        teamSide: String
    },
    data: function() {
        return {
            home_team: '',
            away_team: '',
            data: [],
            headers: [
                {
                    text: this.teamSide,
                    align: 'left',
                    value: 'player_id'
                },
                {
                    text: 'Pelaaja',
                    value: 'first_round.home.player.player_name'
                },
                { value: 'first_round.home.player.score_first' },
                { value: 'first_round.home.player.score_second' },
                { value: 'first_round.home.player.score_third' },
                { value: 'first_round.home.player.score_fourth' },
                { text: 'P', value: 'first_round.home.player.score_total' }
            ]
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
                .then(
                    function(data) {
                        if (this.roundNumber == 1 && this.teamSide == 'home') {
                            this.data = data.body.first_round.home;
                            this.home_team = data.body.home_team.name;
                        } else if (
                            this.roundNumber == 2 &&
                            this.teamSide == 'home'
                        ) {
                            this.data = data.body.second_round.home;
                            this.home_team = data.body.home_team.name;
                        } else if (
                            this.roundNumber == 1 &&
                            this.teamSide == 'away'
                        ) {
                            this.data = data.body.first_round.away;
                            this.away_team = data.body.away_team.name;
                        } else if (
                            this.roundNumber == 2 &&
                            this.teamSide == 'away'
                        ) {
                            this.data = data.body.second_round.away;
                            this.away_team = data.body.away_team.name;
                        }
                        console.log(data.body);
                    },
                    function(error) {
                        console.log(error.statusText);
                    }
                );
        }
    },
    mounted: function() {
        this.getMatch();
    }
};
</script>
