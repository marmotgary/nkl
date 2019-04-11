<template>
  <v-card class="teams">
    <v-layout>
      <v-flex xs12>
        <v-card>
          <v-container grid-list-sm fluid>
            <v-layout row wrap>
              <v-flex xs4 d-flex>
                <v-card flat tile class="d-flex">
                  <v-img
                    :src="`https://picsum.photos/500/300?image=15`"
                    :lazy-src="`https://picsum.photos/10/6?image=15`"
                    aspect-ratio="1"
                    class="grey lighten-2"
                  ></v-img>
                </v-card>
              </v-flex>
              <v-flex xs4 d-flex>
                <v-data-table :headers="headers" :items="teams" hide-actions>
                  <template slot="no-data">
                    <v-progress-linear slot="progress" indeterminate></v-progress-linear>
                  </template>
                  <template bind:key="team.id" slot="items" slot-scope="props">
                    <td>{{ props.item.name }}</td>
                    <td>{{ props.item.abbreviation }}</td>
                    <td>{{ props.item.matches_played }}</td>
                    <td>{{ props.item.matches_won }}</td>
                    <td>{{ props.item.matches_lost }}</td>
                    <td>{{ props.item.matches_tie }}</td>
                    <td>{{ props.item.score_total }}</td>
                  </template>
                </v-data-table>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>

    <v-data-table :headers="headers" :items="players" hide-actions>
      <template slot="no-data">
        <v-progress-linear slot="progress" indeterminate></v-progress-linear>
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
  </v-card>
</template>

<script>
export default {
    data: function() {
        return {
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
            players: []
        };
    },
    methods: {
        getTeams: function() {
            this.$http.get('https://kyykka.rauko.la/api/teams/4').then(
                function(data) {
                    this.teams = data.body;
                    this.players = data.body.players;
                    console.log(this.players);
                },
                function(error) {
                    console.log(error.statusText);
                }
            );
        }
    },
    mounted: function() {
        this.getTeams();
    }
};
</script>
<style scoped>
.teams {
    margin-top: 2em;
}
</style>
