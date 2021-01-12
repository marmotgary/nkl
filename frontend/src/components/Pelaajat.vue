<template>
  <v-card>
    <v-card-title>
      Pelaajat
      <v-spacer></v-spacer>
      <v-text-field color="red" v-model="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>
    <v-data-table mobile-breakpoint="0" disable-pagination dense :headers="headers" :sortDesc="true" :sortBy="sortBy" :items="players" :search="search" hide-default-footer>
      <template slot="no-data">
        <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
      </template>
      <template
        bind:key="props.item.id"
        slot="items"
        slot-scope="props"
      >
        <td>{{ props.item.player_name }}</td>
        <td class="text-xs-left" v-if="props.item.team !== null">{{ props.item.team.abbreviation }}</td>
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
      >Your search for "{{ search }}" found no results.</v-alert>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
    data: function() {
        return {
            search: '',
            sortBy: 'rounds_total',
            sortDesc: false,
            isCaptain: false,
            headers: [
                {
                    text: 'Nimi',
                    value: 'player_name',
                    align: 'left'
                },
                {
                    text: 'Joukkue',
                    value: 'team.abbreviation',
                    align: 'left'
                },
                {
                    text: 'E',
                    value: 'rounds_total',
                    align: 'left'
                },
                { text: 'P', value: 'score_total', width: '1%', align: 'left' },
                {
                    text: 'PPH',
                    value: 'score_per_throw',
                    align: 'left'
                },
                {
                    text: 'SP',
                    value: 'scaled_points',
                    alignt: 'left'
                },
                {
                    text: 'SPe',
                    value: 'scaled_points_per_round',
                    alignt: 'left'
                },
                {
                    text: 'kHP',
                    value: 'avg_throw_turn',
                    align: 'left'
                },
                { text: 'H', value: 'pikes_total', align: 'left' },
                {
                    text: 'H%',
                    value: 'pike_percentage',
                    align: 'left'
                },
                {
                    text: 'VM',
                    value: 'zeros_total',
                    align: 'left'
                },
                {
                    text: 'JK',
                    value: 'gteSix_total',
                    alignt: 'left'
                }
            ],
            players: [],
            selected: []
        };
    },
    methods: {
        getPlayers: function() {
            this.$http.get('api/players/'+'?season='+sessionStorage.season_id).then(
                function(data) {
                    this.players = data.body;
                }
            );
        },
    },
    mounted: function() {
        this.getPlayers();
        if (localStorage.user_id) {
            this.$http.get('api/players/' +localStorage.user_id +'/?season='+sessionStorage.season_id)
        }
    }
};
</script>
<style scoped>

tbody tr :hover {
    cursor: unset;
}

</style>

