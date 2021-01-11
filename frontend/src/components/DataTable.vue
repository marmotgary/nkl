<template>
  <v-card>
    <v-card-title>
      Joukkueet
      <v-spacer></v-spacer>
      <v-text-field color="red" v-model="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>
    <v-data-table disable-pagination @click:row="handleRedirect" dense color='alert' :headers="headers" :search="search" :items="teams" disable-pagination hide-default-footer>
      <template slot="no-data">
        <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
      </template>
      <template bind:key="team.id" slot="items" slot-scope="props">
        <td>
          {{ props.item.name }}
        </td>
        <td>{{ props.item.abbreviation }}</td>
        <td>{{ props.item.matches_played }}</td>
        <td>{{ props.item.matches_won }}</td>
        <td>{{ props.item.matches_lost }}</td>
        <td>{{ props.item.matches_tie }}</td>
        <td>{{ props.item.score_total }}</td>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
    data: function() {
        return {
            search: '',
            headers: [
                { text: 'Nimi', value: 'name', align: 'center' },
                { text: 'Lyhenne', value: 'abbreviation' },
                { text: 'Ottelut', value: 'matches_played' },
                { text: 'Voitot', value: 'matches_won' },
                { text: 'Häviöt', value: 'matches_lost' },
                { text: 'Tasurit', value: 'matches_tie' },
                { text: 'Tehdyt pisteet', value: 'score_total' }
            ],
            teams: []
        };
    },
    methods: {
        getTeams: function() {
            this.$http.get('api/teams/').then(
                function(data) {
                    this.teams = data.body;
                }
            );
        },
        handleRedirect: function(value) {
          location.href = '/joukkue/'+value.id
        }
    },
    mounted: function() {
        this.getTeams();
    }
};
</script>
