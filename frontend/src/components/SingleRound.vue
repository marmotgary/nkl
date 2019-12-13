<template>
  <v-card>
    <v-card-title>Erä {{this.roundNumber}}</v-card-title>
    <v-layout v-if="is_validated" row wrap>
      <v-card-text v-if="this.round_score">
        <p class="text-xs-left" v-if="this.teamSide == 'home'">
          {{this.home_team}}
          <v-chip
            style="float:right;"
            :color="`${this.color} lighten-2`"
            label
            small
          >{{this.round_score}}</v-chip>
        </p>
        <p class="text-xs-left" :color="this.color" v-if="this.teamSide == 'away'">
          {{this.away_team}}
          <v-chip
            style="float:right;"
            :color="`${this.color} lighten-2`"
            label
            small
          >{{this.round_score}}</v-chip>
        </p>
      </v-card-text>
    </v-layout>
    <v-layout v-if="!is_validated" row wrap>
      <v-card-text v-if="this.round_score">
        <!-- Tähän dynaaminen pisteiden lisäys -->
        <p class="text-xs-left" v-if="this.teamSide == 'home'">
          {{this.home_team}}
          <v-chip
            style="float:right;"
            :color="`${this.color} lighten-2`"
            label
            small
          >{{this.round_score}}</v-chip>
        </p>
        <p class="text-xs-left" :color="this.color" v-if="this.teamSide == 'away'">
          {{this.away_team}}
          <v-chip
            style="float:right;"
            :color="`${this.color} lighten-2`"
            label
            small
          >{{this.round_score}}</v-chip>
        </p>
      </v-card-text>
    </v-layout>
    <v-data-table
      v-if="is_validated"
      disable-initial-sort
      :headers="headers"
      :items="data"
      hide-actions
    >
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
        <td v-if="props.item.score_total">{{props.item.score_total}}</td>
      </template>
    </v-data-table>
    <v-data-table
      v-if="!is_validated"
      disable-initial-sort
      :headers="headers"
      :items="data"
      hide-actions
      :pagination.sync="pagination"
      >
      <template slot="items">
        <!-- Here you put the id according to the player selected on the next column !-->
        <tr>
          <td>69</td>
          <td>
            <v-select v-if="this.teamSide == 'home'" class="text-center pr-1" v-bind:value="home_players[0]" :items="home_players" @change="disablePlayer" single-line></v-select>
            <v-select v-else-if="this.teamSide == 'away'" class="text-center pr-1" v-bind:value="away_players[0]" :items="away_players" @change="disablePlayer" single-line></v-select>
          </td>
          <td>
            <v-edit-dialog class="text-center pr-1">0</v-edit-dialog>
          </td>
          <td>
            <v-edit-dialog class="text-center pr-1">0</v-edit-dialog>
          </td>
          <td>
            <v-edit-dialog class="text-center pr-1">0</v-edit-dialog>
          </td>
          <td>
          <v-edit-dialog class="text-center pr-1">0</v-edit-dialog>
          </td>
          <td>
            {{this.player_scores}}
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-card>
</template>
<style scoped>
td {
  padding: 0 !important;
  text-align: center !important;
}
</style>



<script>
export default {
    name: 'match-round',
    props: {
        roundNumber: String,
        teamSide: String
    },
    data: function() {
        return {
            pagination: {
              rowsPerPage: 4
            },
            home_team: '',
            away_team: '',
            round_score: '',
            player_scores: 0,
            color: '',
            is_validated: '',
            throw_score: 0,
            home_players: [],
            away_players: [],
            data: [],
            headers: [
                {
                    text: this.teamSide,
                    value: 'player_id',
                    sortable: false,
                    width: '5%'
                },
                {
                    text: 'player',
                    value: 'player',
                    sortable: false,
                    width: '35%'
                },
                { value: 'score_first', sortable: false, width: '10%'},
                { value: 'score_second', sortable: false, width: '10%'},
                { value: 'score_third', sortable: false, width: '10%'},
                { value: 'score_fourth', sortable: false, width: '10%'},
                { text: 'Pts.', align: 'center',value: 'score_total', width: '5%'}
            ],
            options: {
              itemsPerPage:4,
            }
        };
    },
    methods: {
        countTotal: function(val) {
          this.player_scores += val
        },
        disablePlayer: function(player) {
          // this.selected.push(player)
          // this.players = this.players.filter( ( el ) => !this.selected.includes( el ) );
        },
        increment: function() {
            this.throw_score = parseInt(this.throw_score, 10) + 1;
        },
        decrement: function() {
            this.throw_score = parseInt(this.throw_score, 10) - 1;
        },
        getMatch: function() {
            this.$http
                .get(
                    'http://localhost:8000/api/matches/' +
                        this.$route.fullPath.substr(
                            this.$route.fullPath.lastIndexOf('/') + 1
                        )
                )
                .then(
                    function(data) {
                        this.is_validated = data.body.is_validated;
                        if (this.roundNumber == 1 && this.teamSide == 'home') {
                            this.data = data.body.first_round.home;
                            this.home_team = data.body.home_team.name;
                            this.round_score = data.body.home_first_round_score;
                            if (
                                this.round_score >
                                data.body.away_first_round_score
                            ) {
                                this.color = 'red';
                            } else {
                                this.color = 'green';
                            }
                        } else if (
                            this.roundNumber == 2 &&
                            this.teamSide == 'home'
                        ) {
                            this.data = data.body.second_round.home;
                            this.home_team = data.body.home_team.name;
                            this.round_score =
                                data.body.home_second_round_score;
                            if (
                                this.round_score >
                                data.body.away_second_round_score
                            ) {
                                this.color = 'red';
                            } else {
                                this.color = 'green';
                            }
                        } else if (
                            this.roundNumber == 1 &&
                            this.teamSide == 'away'
                        ) {
                            this.data = data.body.first_round.away;
                            this.away_team = data.body.away_team.name;
                            this.round_score = data.body.away_first_round_score;
                            if (
                                this.round_score >
                                data.body.home_first_round_score
                            ) {
                                this.color = 'red';
                            } else {
                                this.color = 'green';
                            }
                        } else if (
                            this.roundNumber == 2 &&
                            this.teamSide == 'away'
                        ) {
                            this.data = data.body.second_round.away;
                            this.away_team = data.body.away_team.name;
                            this.round_score =
                                data.body.away_second_round_score;
                            if (
                                this.round_score >
                                data.body.home_second_round_score
                            ) {
                                this.color = 'red';
                            } else {
                                this.color = 'green';
                            }
                        }
                        var arr_home = [];
                        var arr_away = [];
                        data.body.home_team.players.forEach(function(player) {
                            arr_home.push(player.player_name);
                        });
                        data.body.away_team.players.forEach(function(player) {
                          arr_away.push(player.player_name);
                        });
                        this.home_players = arr_home;
                        this.away_players = arr_away;
                        console.log(this.data)
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
