<template>
  <v-card class="teams">
    <v-layout>
      <v-flex xs12>
        <v-card>
          <v-container grid-list-sm fluid>
            <v-flex xs4 mb-4 d-flex offset-sm4>
              <v-card flat tile class="d-flex">
                <v-img
                  :src="`https://picsum.photos/id/237/200/300`"
                  aspect-ratio="1"
                  max-height="200"
                  max-width="300"
                  class="grey lighten-2"
                ></v-img>
              </v-card>
            </v-flex>
            <v-flex xs12 d-flex>
              <v-data-iterator
                :items="stats"
                :headers="header"
                content-tag="v-layout"
                hide-actions
                row
                wrap
              >
                <template v-slot:header>
                  <v-toolbar class="mb-2" color="red darken-5" dark flat>
                    <v-toolbar-title>{{header}}</v-toolbar-title>
                  </v-toolbar>
                </template>
                <template v-slot:item="props">
                  <v-flex xs12>
                    <v-card>
                      <v-list dense>
                        <v-list-tile>
                          <v-list-tile-content>Tehdyt pisteet:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.score_total }}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content>Ottelut:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.match_count }}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content>Hauet:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.pikes_total }}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content>Nolla heitot:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.zeros_total }}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content>Nolla aloitukset:</v-list-tile-content>
                          <v-list-tile-content
                            class="align-end"
                          >{{ props.item.zero_first_throw_total }}</v-list-tile-content>
                        </v-list-tile>
                      </v-list>
                    </v-card>
                  </v-flex>
                </template>
              </v-data-iterator>
              <v-data-iterator :items="stats" content-tag="v-layout" hide-actions row wrap>
                <template v-slot:header>
                  <v-toolbar class="mb-2" color="red darken-5" dark flat>
                    <v-toolbar-title></v-toolbar-title>
                  </v-toolbar>
                </template>
                <template v-slot:item="props">
                  <v-flex xs12>
                    <v-card>
                      <v-list dense>
                        <v-list-tile>
                          <v-list-tile-content>Heitot:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.throws_total }}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content>Pistettä per heitto:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.score_per_throw }}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content>Haukiprosentti:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.pike_percentage }}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content>Nollaprosentti:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.zero_percentage }}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content>Joulukuuset:</v-list-tile-content>
                          <v-list-tile-content class="align-end">{{ props.item.gteSix_total }}</v-list-tile-content>
                        </v-list-tile>
                      </v-list>
                    </v-card>
                  </v-flex>
                </template>
              </v-data-iterator>
            </v-flex>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
    <v-data-table :headers="headers" :items="players" hide-actions>
      <template slot="no-data">
        <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
      </template>
      <template slot="items" slot-scope="props">
        <td>{{ props.item.id }}</td>
        <td>{{ props.item.player_name }}</td>
        <td>{{ props.item.rounds_total }}</td>
        <td>{{ props.item.score_total }}</td>
        <td>{{ props.item.score_per_throw }}</td>
        <td>{{ props.item.scaled_points }}</td>
        <td>{{ props.item.scaled_points_per_round }}</td>
        <td>{{ props.item.avg_throw_turn }}</td>
        <td>{{ props.item.pike_percentage }}</td>
        <td>{{ props.item.zeros_total }}</td>
        <td>{{ props.item.gteSix_total }}</td>
      </template>
    </v-data-table>
    <v-spacer></v-spacer>
    <v-card>
      <v-expansion-panel v-if="isCaptain">
        <v-expansion-panel-content>
          <template v-slot:header>
            <div>Varaa pelaajia</div>
          </template>
          <v-card>
            <v-data-table :items="reserve" :headers="reserveHeaders" hide-actions>
              <template slot="no-data">
                <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
              </template>
              <template slot="items" slot-scope="props">
                <div class="row">
                  <td v-if="props.item.team == null">
                    <v-btn v-on:click="reserveButton(props.index)" flat icon color="green">
                      <v-icon>fas fa-plus</v-icon>
                    </v-btn>
                  </td>
                  <td v-else>
                    <v-btn flat disabled icon color="gray">
                      <v-icon>fas fa-lock</v-icon>
                    </v-btn>
                  </td>
                </div>
                <td>{{ props.item.id }}</td>
                <td>{{ props.item.player_name }}</td>
              </template>
            </v-data-table>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-card>
  </v-card>
</template>

<script>
export default {
    data: function() {
        return {
            header: '',
            isCaptain: false,
            team_id: this.$route.fullPath.substr(
                this.$route.fullPath.lastIndexOf('/') + 1
            ),
            reserveHeaders: [
                {
                    text: 'Varaa',
                    value: 'reserve',
                    width: '1%',
                    align: 'left'
                },
                { text: '#', value: 'id' },
                { text: 'Pelaajan nimi', value: 'player_name' }
            ],
            headers: [
                { text: '#', value: 'id' },
                {
                    text: 'Nimi',
                    value: 'player_name',
                    width: '1%',
                    align: 'left'
                },
                {
                    text: 'E',
                    value: 'rounds_total',
                    width: '1%',
                    align: 'left'
                },
                { text: 'P', value: 'score_total', width: '1%', align: 'left' },
                {
                    text: 'PPH',
                    value: 'score_per_throw',
                    width: '1%',
                    align: 'left'
                },
                {
                    text: 'SP',
                    value: 'scaled_points',
                    width: '1%',
                    alignt: 'left'
                },
                {
                    text: 'SPe',
                    value: 'scaled_points_per_round',
                    width: '1%',
                    alignt: 'left'
                },
                {
                    text: 'kHP',
                    value: 'avg_throw_turn',
                    width: '1%',
                    align: 'left'
                },
                { text: 'H', value: 'pikes_total', width: '1%', align: 'left' },
                {
                    text: 'H%',
                    value: 'pike_percentage',
                    width: '1%',
                    align: 'left'
                },
                {
                    text: 'VM',
                    value: 'zeros_total',
                    width: '1%',
                    align: 'left'
                },
                {
                    text: 'JK',
                    value: 'gteSix_total',
                    width: '1%',
                    alignt: 'left'
                }
            ],
            stats: [],
            players: [],
            reserve: []
        };
    },
    methods: {
        getPlayers: function() {
            this.$http
                .get('http://localhost:8000/api/teams/' + this.team_id)
                .then(
                    function(data) {
                        this.stats = [data.body];
                        this.players = data.body.players;
                        this.header = data.body.name;
                    },
                );
        },
        getReserve: function() {
            this.$http.get('http://localhost:8000/api/reserve/').then(
                function(data) {
                    var i = 0;
                    for (var player in data.body) {
                        if (data.body[i].team == null) {
                            this.reserve.push(data.body[i]);
                        }
                        i++;
                    }
                },
                function(error) {
                    console.log(error.statusText);
                }
            );
        },
        reserveButton: function(index) {
            let post_data = {'player': this.reserve[index].id}
            let post_url = 'http://localhost:8000/api/reserve/'
            if (confirm('Haluatko varmasti varata tämän pelaajan?')) {
              this.$http.post(post_url, post_data, {
                headers: {
                  'X-CSRFToken': this.getCookie('csrftoken')
                },
                  'withCredentials': true,        
                }).then(function(response) {
                  if (response.status === 200) {
                      this.getPlayers();
                      this.reserve.splice(index, 1);
                  }
                }).catch(function(response) {
                  if (response.status == 403) {
                    this.$http
                      .get('http://localhost:8000/api/csrf', {'withCredentials': true})
                      .then(function(response) {
                          if (response.status === 200) {
                              this.getPlayers();
                              this.reserve.splice(index, 1);
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
            }
        }
    },
    mounted: function() {
        this.header = '';
        this.getPlayers();
        if (this.$session.get('user_id') && this.$session.get('role_id') == 1) {
            this.getReserve();
            this.isCaptain = true;
        }
    }
};
</script>
<style scoped>
.teams {
    margin-top: 2em;
}
</style>
