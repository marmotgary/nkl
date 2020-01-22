<template>
  <v-card>
    <v-card-title>Erä {{this.roundNumber}}<v-spacer/><v-progress-circular :size="20" :width="2" indeterminate color="red" v-if="loading"/></v-card-title>
    <v-layout v-if="!show_input" row wrap>
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
    <v-layout v-if="show_input" row wrap>
      <v-card-text v-if="loaded">
        <p class="text-xs-left" v-if="this.teamSide == 'home'">
          {{this.home_team}}
          <v-text-field @input="roundScore()" style="width:10%; float:right;" v-model="round_score" class="centered-input" maxlength="3"/>
        </p>
        <p class="text-xs-left" :color="this.color" v-if="this.teamSide == 'away'">
          {{this.away_team}}
          <v-text-field @input="roundScore()" style="width:10%; float:right;" v-model="round_score" class="centered-input" maxlength="3"/>
        </p>
      </v-card-text>
    </v-layout>
    <v-data-table
      v-if="!show_input"
      disable-initial-sort
      :headers="headers"
      :items="data"
      hide-actions
    >
      <template slot="no-data">
        <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
      </template>
      <template slot="headers" class="text-xs-center"></template>
      <template slot="items" slot-scope="props">
        <td>{{props.item.player.player_number}}</td>
        <td>{{props.item.player.player_name}}</td>
        <td>{{props.item.score_first}}</td>
        <td>{{props.item.score_second}}</td>
        <td>{{props.item.score_third}}</td>
        <td>{{props.item.score_fourth}}</td>
        <td>{{props.item.score_total}}</td>
      </template>
    </v-data-table>
    <v-data-table
      v-if="show_input"
      disable-initial-sort
      v-model="select"
      :headers="headers"
      :items="data"
      hide-actions
      :pagination.sync="pagination"
      >
      <template slot="no-data">
        <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
      </template>
      <template slot="headers" class="text-xs-center"></template>
      <template slot="items" slot-scope="props">
        <td :ref="'id_'+props.index">{{selected[props.index].player.id}}</td>
        <td>
          <v-select v-model="selected[props.index].player.player_name" @change="loadPlayer($event, props.index)" v-if="teamSide == 'home'" class="text-center pr-1" placeholder="Select player" :items="home_players" single-line></v-select>
          <v-select v-model="selected[props.index].player.player_name" @change="loadPlayer($event, props.index)" v-else-if="teamSide == 'away'" class="text-center pr-1" placeholder="Select player" :items="away_players" single-line></v-select>
        </td>
        <td><v-text-field v-model="selected[props.index]['score_first']" :ref="'first_throw_'+props.index" class="centered-input" maxlength="2" @input="sumTotal(props.index)" v-on:keypress="isNumber($event)"/></td>
        <td><v-text-field v-model="selected[props.index]['score_second']" :ref="'second_throw_'+props.index" class="centered-input" maxlength="2" @input="sumTotal(props.index)" v-on:keypress="isNumber($event)"/></td>
        <td><v-text-field v-model="selected[props.index]['score_third']" :ref="'third_throw_'+props.index" class="centered-input" maxlength="2" @input="sumTotal(props.index)" v-on:keypress="isNumber($event)"/></td>
        <td><v-text-field v-model="selected[props.index]['score_fourth']" :ref="'fourth_throw_'+props.index" class="centered-input" maxlength="2" @input="sumTotal(props.index)" v-on:keypress="isNumber($event)"/></td>
        <td class="centered-input" style="font-size:18px" :ref="'throw_sum_'+props.index">{{selected[props.index]['score_total']}}</td>
      </template>
    </v-data-table>
  </v-card>
</template>
<style scoped>

  td {
    padding: 0 !important;
    text-align: center !important;
  }

  .centered-input >>> input {
    text-align: center
  }

  .v-text-field {
    font-size: 1.1em !important;
  }
</style>



<script>
export default {
    name: 'match-round',
    props: {
        matchData: Object,
        roundNumber: String,
        teamSide: String,
    },
    data: function() {
        return {
            pagination: {
              rowsPerPage: 4
            },
            select: [],
            selected: [],
            show_input: false,
            loading: false,
            loaded: false,
            home_team: '',
            away_team: '',
            round_score: '',
            color: '',
            is_validated: '',
            home_players: [],
            away_players: [],
            data: [],
            plain_data: [],
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
                { text: 1, value: 'score_first', sortable: false, width: '10%'},
                { text: 2, value: 'score_second', sortable: false, width: '10%'},
                { text: 3, value: 'score_third', sortable: false, width: '10%'},
                { text: 4, value: 'score_fourth', sortable: false, width: '10%'},
                { text: 'Pts.', align: 'center', sortable: false, value: 'score_total', width: '5%'}
            ],
            options: {
              itemsPerPage: 4,
            }
        };
    },
    methods: {
        isNumber: function(evt) {
          // Checks that the value is an H or a numeric value from the ASCII table.
          evt = (evt) ? evt : window.event;
          var charCode = (evt.which) ? evt.which : evt.keyCode;
          if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 72 && charcode !== 104) {
            evt.preventDefault();
          } else {
            return true;
          }
        },
        roundScore: function() {
          let post_url = 'api/matches/'+this.plain_data.body.id
          let post_data = {}
          let key = ''

          if (this.teamSide == 'home') {
            key = (this.roundNumber==1) ? "home_first_round_score" : "home_second_round_score";
          } else if (this.teamSide == 'away') {
            key = (this.roundNumber==1) ? "away_first_round_score" : "away_second_round_score";
          }
          post_data[key] = this.round_score
          this.$http.patch(post_url, post_data, {
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken')
            },
              'withCredentials': true,        
            }).then().catch(function(response) {
              if (response.status == 403) {
                this.$http
                  .get('api/csrf', {'withCredentials': true})
                  .then(function(response) {
                      if (response.status === 200) {
                          this.$http.patch(post_url, post_data, {
                          headers: {
                            'X-CSRFToken': this.getCookie('csrftoken')
                          },
                            'withCredentials': true,
                          })
                      }
                  });
              }
            })
        },
        sumTotal: function(index) {
          /* The function loops through all the column elements of the corresponding row
          and adds them up as total to the last column. The function also updates the database
          accordingly on each runthrough. */
          this.loading = true

          let throws;
          let total = 0;
          const array = [
            'first',
            'second',
            'third',
            'fourth'
          ]

          let post_data = 
          {
          "score_first": 0,
          "score_second": 0,
          "score_third": 0,
          "score_fourth": 0,
          "player": this.$refs['id_'+index].firstChild.data
          }

          if (this.teamSide == 'home') {
            throws = (this.roundNumber==1) ? [0,1,2,3] : [8,9,10,11];
          } else if (this.teamSide == 'away') {
            throws = (this.roundNumber==1) ? [4,5,6,7] : [12,13,14,15];
          }

          array.forEach(function (item) {
            const element = this.$refs[item+'_throw_'+index].$refs.input.value
            if(element.toLowerCase() == "h") {
              total += 0
              var score = "h";
            }else{
              var score = (!isNaN(parseInt(element))) ? parseInt(element) : 0;
              total += score
            }
            if (element.length > 0) {
              post_data['score_'+item] = score
            }
          }, this);

          this.$refs['throw_sum_'+index].firstChild.data = total

          let post_url = 'api/throws/update/'+this.data[index].id+'/'

          this.$http.patch(post_url, post_data, {
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken')
            },
            'withCredentials': true,
            }).then(
              setTimeout(() => {
                this.loading = false
              }, 500)
            ).catch(error => {
              setTimeout(() => {
                this.loading = false
              }, 500);
            }).catch(function(response) {
              if (response.status == 403) {
                this.$http
                  .get('api/csrf', {'withCredentials': true})
                  .then(function(response) {
                      if (response.status === 200) {
                          this.$http.patch(post_url, post_data, {
                          headers: {
                            'X-CSRFToken': this.getCookie('csrftoken')
                          },
                          'withCredentials': true,
                          })
                      }
                  });
              }
            })
        },
        loadPlayer: function(player, index) {
          // Finds the selected player object from the dataset and sets it's id to the id field. 
          let obj = this.plain_data.body[this.teamSide + "_team"].players.find(o => o.player_name === player)
          this.$refs['id_'+index].innerHTML=obj.id
          this.select = []
          this.disabled[index] = false
          this.sumTotal(index)
        },
        getMatch: function() {
          this.plain_data = this.matchData
          this.is_validated = this.matchData.body.is_validated;
          if (this.roundNumber == 1 && this.teamSide == 'home') {
              this.data = this.matchData.body.first_round.home;
              this.home_team = this.matchData.body.home_team.name;
              this.round_score = this.matchData.body.home_first_round_score;
              if (
                  this.round_score >
                  this.matchData.body.away_first_round_score
              ) {
                  this.color = 'red';
              } else {
                  this.color = 'green';
              }
          } else if (
              this.roundNumber == 2 &&
              this.teamSide == 'home'
          ) {
              this.data = this.matchData.body.second_round.home;
              this.home_team = this.matchData.body.home_team.name;
              this.round_score =
                  this.matchData.body.home_second_round_score;
              if (
                  this.round_score >
                  this.matchData.body.away_second_round_score
              ) {
                  this.color = 'red';
              } else {
                  this.color = 'green';
              }
          } else if (
              this.roundNumber == 1 &&
              this.teamSide == 'away'
          ) {
              this.data = this.matchData.body.first_round.away;
              this.away_team = this.matchData.body.away_team.name;
              this.round_score = this.matchData.body.away_first_round_score;
              if (
                  this.round_score >
                  this.matchData.body.home_first_round_score
              ) {
                  this.color = 'red';
              } else {
                  this.color = 'green';
              }
          } else if (
              this.roundNumber == 2 &&
              this.teamSide == 'away'
          ) {
              this.data = this.matchData.body.second_round.away;
              this.away_team = this.matchData.body.away_team.name;
              this.round_score =
                  this.matchData.body.away_second_round_score;
              if (
                  this.round_score >
                  this.matchData.body.home_second_round_score
              ) {
                  this.color = 'red';
              } else {
                  this.color = 'green';
              }
          }
          var arr_selected = [];
          var arr_home = [];
          var arr_away = [];

          this.data.forEach(function (item) {
            arr_selected.push(item)
          })
          this.matchData.body.home_team.players.forEach(function(player) {
            arr_home.push(player.player_name);
          });
          this.matchData.body.away_team.players.forEach(function(player) {
            arr_away.push(player.player_name);
          });
          this.selected = arr_selected;
          this.home_players = arr_home;
          this.away_players = arr_away;
          this.loaded = true
          
          if(!this.is_validated) {
            if (localStorage.team_id == this.plain_data.body.home_team.id) {
              this.show_input = (localStorage.role_id==1) ? true : false;
            }
          }
        }
    },
    mounted: function() {
      this.getMatch();
    }
};
</script>
