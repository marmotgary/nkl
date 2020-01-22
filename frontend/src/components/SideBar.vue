<template>
  <v-card class="teams">
    <v-card-title>
      Joukkueet
      <v-spacer></v-spacer>
    </v-card-title>
    <v-flex xs12>
      <v-data-table :headers="headers" :items="teams" v-bind:pagination.sync="pagination" hide-actions>
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
    </v-flex>
  </v-card>
</template>

<script>
export default {
    data: function() {
        return {
            headers: [
                { text: 'Joukkue', value: 'abbreviation', sortable: false},
                { text: 'O', value: 'matches_played', sortable: false},
                { text: 'V', value: 'matches_won', sortable: false},
                { text: 'H', value: 'matches_lost', sortable: false},
                { text: 'T', value: 'matches_tie', sortable: false},
                { text: 'P', value: 'points_total'}
            ],
            pagination: {'sortBy': 'points_total', 'descending': true, 'rowsPerPage': -1},
            teams: []
        };
    },
    methods: {
        getTeams: function() {
            this.$http.get('api/teams/').then(
                function(data) {
                    this.teams = data.body;
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
<style>
tbody tr:nth-of-type(odd) {
    background-color: rgba(0, 0, 0, 0.05);
}
</style>
