<template>
  <v-card>
    <v-data-table mobile-breakpoint="0" :header-props="{ sortIcon: null }" disable-pagination @click:row="handleRedirect" dense :headers="headers" :items="teams" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" hide-default-footer>
      <template slot="no-data">
        <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
      </template>
      <template slot="items" slot-scope="props">
        <td>{{ props.item.abbreviation }}</td>
        <td>{{ props.item.matches_played }}</td>
        <td>{{ props.item.matches_won }}</td>
        <td>{{ props.item.matches_lost }}</td>
        <td>{{ props.item.matches_tie }}</td>
        <td>{{ props.item.points_total }}</td>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
    data: function() {
        return {
            sortBy: 'points_total',
            sortDesc: true,
            headers: [
                { text: 'Joukkue', value: 'abbreviation', sortable: false},
                { text: 'O', value: 'matches_played', sortable: false},
                { text: 'V', value: 'matches_won', sortable: false},
                { text: 'H', value: 'matches_lost', sortable: false},
                { text: 'T', value: 'matches_tie', sortable: false},
                { text: 'P', value: 'points_total'}
            ],
            teams: []
        };
    },
    methods: {
        getTeams: function() {
            this.$http.get('api/teams/'+'?season='+sessionStorage.season_id).then(
                function(data) {
                    this.teams = data.body;
                },
                function(error) {
                    console.log(error.statusText);
                }
            );
        },
        handleRedirect: function(value) {
          location.href = '/joukkue/'+value.id;
        }
    },
    mounted: function() {
        this.getTeams();
    }
};
</script>
<style>

</style>
