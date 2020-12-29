<template>
  <v-card>
    <v-card-title class="d-flex flex-wrap-reverse">
      <div>
        Ottelut
        <v-select v-on:input="selectChange()" v-model="defaultSelected" style="width: 50%" color="red" :items="options">
        </v-select>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-text-field color="red" v-model="search" label="Search" single-line hide-details></v-text-field>             
      </div>
    </v-card-title>
    <v-data-table disable-pagination @click:row="handleRedirect" dense :headers="headers" :items="data" :search="search" hide-default-footer>
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
            data: [],
            matches: [],
            post_season: [],
            regular_season: [],
            defaultSelected: 'Kaikki ottelut',
            options: ['Kaikki ottelut','Runkosarja','Jatkosarja'],
        };
    },
    methods: {
        selectChange: function() {
          if (this.defaultSelected == "Runkosarja") {
            this.data = this.regular_season
          } else if (this.defaultSelected == "Jatkosarja") {
            this.data = this.post_season
          } else {
            this.data = this.matches
          }
        },
        getMatches: function() {
          let url = 'api/matches/';
          let i = 0;

          this.$http.get(url).then(
              function(data) {
                  this.data = data.body;
                  this.matches = data.body;
                  for (let object in data.body) {
                    if (data.body[i].post_season) {
                      this.post_season.push(data.body[i]);
                    } else {
                      this.regular_season.push(data.body[i]);
                    }
                    i++;
                  }
              }
          );
        },
        handleRedirect: function(value) {
          location.href = '/ottelu/'+value.id
        }
    },
    mounted: function() {
        this.getMatches();
    }
};
</script>

