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
      >
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
                { text: 'PPO', value: 'score_total', align: 'left' },
                {
                    text: 'PPH',
                    value: 'score_per_throw',
                    align: 'left'
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
                    align: 'left',
                    width: '1%'
                },
                {
                    text: 'JK',
                    value: 'gteSix_total',
                    alignt: 'left',
                    width: '1%'
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
                    if (data) {
                        // TODO: This should prolly be done in django and not in frontend.
                        let new_data = data.body.map(function(obj) {
                            obj['score_total'] = parseFloat(obj['score_total'] / obj['rounds_total']).toFixed(2);
                            return obj;
                        })

                        this.players = new_data;
                    }
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

