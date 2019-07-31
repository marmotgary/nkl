<template>
  <v-card class="teams">
    <v-card-title>
      Joukkueet
      <v-spacer></v-spacer>
    </v-card-title>
    <v-flex xs12>
      <v-data-table :headers="headers" :items="teams" hide-actions>
        <template slot="no-data">
          <v-progress-linear slot="progress" indeterminate></v-progress-linear>
        </template>
        <template bind:key="team.id" slot="items" slot-scope="props">
          <td class="block">{{ props.item.abbreviation }}</td>
          <td class="block">{{ props.item.matches_played }}</td>
          <td class="block">{{ props.item.matches_won }}</td>
          <td class="block">{{ props.item.matches_lost }}</td>
          <td class="block">{{ props.item.matches_tie }}</td>
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
                { text: 'Joukkue', value: 'abbreviation' },
                { text: 'O', value: 'matches_played' },
                { text: 'V', value: 'matches_won' },
                { text: 'H', value: 'matches_lost' },
                { text: 'T', value: 'matches_tie' }
            ],
            teams: []
        };
    },
    methods: {
        getTeams: function() {
            this.$http.get('https://kyykka.rauko.la/api/teams/').then(
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
