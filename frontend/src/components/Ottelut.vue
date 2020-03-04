<template>
  <v-card>
    <v-card-title class="d-flex flex-wrap-reverse">
      <div class="order-1">
        Ottelut
        <v-select v-on:input="selectChange(`${select.src}`)" v-model="defaultSelected" style="width: 50%" color="red" :items="options">
        </v-select>
      </div>
      <div class="order-2">
        <v-text-field color="red" v-model="search" label="Search" single-line hide-details></v-text-field>             
      </div>
    </v-card-title>
    <v-data-table :headers="headers" :items="matches" :search="search" hide-actions>
      <template slot="no-data">
        <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
      </template>
      <template slot="headers" class="text-xs-center"></template>
      <template slot="items" slot-scope="props">
        <router-link :to="'ottelu/'+props.item.id">
          <td class="time"><a>{{ props.item.match_time | moment('YYYY-MM-DD HH:mm') }}</a></td>
        </router-link>
        <td class="text-xs-left">{{ props.item.field }}</td>
        <td class="text-xs-left">{{ props.item.home_team.abbreviation }}</td>
        <td class="text-xs-left">{{ props.item.away_team.abbreviation }}</td>
        <td
          class="text-xs-left"
          v-if="props.item.home_score_total && props.item.away_score_total"
        >{{ props.item.home_score_total + '-' + props.item.away_score_total }}</td>
        <td v-else class="text-xs-center">-</td>
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

// /api/matches/?post_season=1

export default {
    data: function() {
        return {
            search: '',
            headers: [
                {
                    text: 'Aika',
                    align: 'left',
                    value: 'match_time'
                },
                { text: 'Kenttä', value: 'field'},
                { text: 'Koti', value: 'home_team.abbreviation' },
                { text: 'Vieras', value: 'away_team.abbreviation' },
                { text: 'Tulos', sortable: false }
            ],
            matches: [],
            defaultSelected: 'Kaikki ottelut',
            options: ['Kaikki ottelut','Runkosarja','Jatkosarja']
        };
    },
    methods: {
        getMatches: function() {
            this.$http.get('api/matches/').then(
                function(data) {
                    this.matches = data.body;
                }
            );
        },
        selectChange: function(jau) {
           console.log(this.defaultSelected)
           console.log(jau)
        }
    },
    mounted: function() {
        this.getMatches();
    }
};
</script>

