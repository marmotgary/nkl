<template>
  <v-card>
    <v-card-title>
      Pelaajat
      <v-spacer></v-spacer>
      <v-text-field v-model="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>
    <v-data-table :headers="headers" :items="players" :search="search" hide-actions>
      <template slot="no-data">
        <v-progress-linear slot="progress" indeterminate></v-progress-linear>
      </template>
      <template
        v-if="props.item.rounds_total > 0"
        bind:key="props.item.id"
        slot="items"
        slot-scope="props"
      >
        <td>{{ props.item.player_name }}</td>
        <td class="text-xs-left" v-if="props.item.team !== null">{{ props.item.team.name }}</td>
        <td v-else>Ei varausta</td>
        <td class="text-xs-left">{{ props.item.rounds_total }}</td>
        <td class="text-xs-left">{{ props.item.score_total }}</td>
        <td class="text-xs-left">{{ props.item.score_per_throw }}</td>
        <td class="text-xs-left">{{ props.item.scaled_points }}</td>
        <td class="text-xs-left">{{ props.item.scaled_points_per_round }}</td>
        <td class="text-xs-left">{{ props.item.avg_throw_turn }}</td>
        <td class="text-xs-left">{{ props.item.pikes_total }}</td>
        <td class="text-xs-left">{{ props.item.pike_percentage }}</td>
        <td class="text-xs-left">{{ props.item.zeros_total }}</td>
        <td class="text-xs-left">{{ props.item.gteSix_total }}</td>
      </template>
      <v-alert
        slot="no-results"
        :value="true"
        color="error"
        icon="warning"
      >Your search for "{{ search }}" found no results.</v-alert>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
    data: function() {
        return {
            search: '',
            isCaptain: false,
            headers: [
                {
                    text: 'Nimi',
                    value: 'player_name',
                    width: '1%',
                    align: 'left'
                },
                {
                    text: 'Joukkue',
                    value: 'team.name',
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
            players: [],
            selected: []
        };
    },
    methods: {
        getPlayers: function() {
            this.$http.get('https://kyykka.rauko.la/api/players/').then(
                function(data) {
                    this.players = data.body;
                    console.log(this.players);
                },
                function(error) {
                    console.log(error.statusText);
                }
            );
        },
        reservePlayer: function() {
            this.$http
                .post('https://kyykka.rauko.la/api/reserve/')
                .then(function(response) {});
        }
    },
    mounted: function() {
        this.getPlayers();
        if (this.$session.get('user_id')) {
            this.$http
                .get(
                    'https://kyykka.rauko.la/api/players/' +
                        this.$session.get('user_id')
                )
                .then(function(response) {
                    console.log(response);
                    // this.isCaptain = !this.isCaptain;
                });
        }
    }
};
</script>
<style>
.v-table tbody td:not(:last-child) {
    border-right: solid #c5c5c5 1px;
}
</style>
