<template>
  <v-card>
    <v-card-title>Erä {{this.roundNumber}}</v-card-title>
    <v-data-table :headers="headers" :items="data" hide-actions>
      <template slot="no-data">
        <v-progress-linear slot="progress" indeterminate></v-progress-linear>
      </template>
      <template slot="headers" class="text-xs-center"></template>
      <template slot="item" slot-scope="props">
        <td v-for="i in props.item" :key="i.id" class="text-xs-left">{{i.player.id}}</td>
      </template>
      <template slot="headers" class="text-xs-center"></template>
      <template></template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
    name: 'match-round',
    props: {
        roundNumber: String,
        teamSide: String
    },
    data: function() {
        return {
            data: [],
            headers: [
                {
                    text: this.teamSide,
                    align: 'left',
                    value: 'player_id'
                },
                {
                    text: 'Pelaaja',
                    value: 'first_round.home.player.player_name'
                },
                { value: 'first_round.home.player.score_first' },
                { value: 'first_round.home.player.score_second' },
                { value: 'first_round.home.player.score_third' },
                { text: 'P', value: 'first_round.home.player.score_fourth' }
            ]
        };
    },
    methods: {
        getMatch: function() {
            this.$http
                .get(
                    'https://kyykka.rauko.la/api/matches/' +
                        this.$route.fullPath.substr(
                            this.$route.fullPath.lastIndexOf('/') + 1
                        )
                )
                .then(
                    function(data) {
                        if (this.roundNumber == 1 && this.teamSide == 'home') {
                            var data = data.body.first_round.home;
                        } else if (
                            this.roundNumber == 2 &&
                            this.teamSide == 'home'
                        ) {
                            var data = data.body.second_round.home;
                        } else if (
                            this.roundNumber == 1 &&
                            this.teamSide == 'away'
                        ) {
                            var data = data.body.first_round.away;
                        } else if (
                            this.roundNumber == 2 &&
                            this.teamSide == 'away'
                        ) {
                            var data = data.body.second_round.away;
                        }
                        console.log(data);
                    },
                    function(error) {
                        console.log(error.statusText);
                    }
                );
        }
    },
    mounted: function() {
        this.getMatch();
    }
};
</script>
