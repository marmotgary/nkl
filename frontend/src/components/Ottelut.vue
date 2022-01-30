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
    <v-data-table mobile-breakpoint="0" disable-pagination @click:row="handleRedirect" dense 
    :headers="headers" :items="data" :search="search" :item-class="itemRowBackground" hide-default-footer>
        <template slot="no-data">
          <v-progress-linear color="red" slot="progress" indeterminate></v-progress-linear>
        </template>
        <template slot="headers" class="text-xs-center"></template>
        <!-- [``] needed to prevent eslint error -->
        <template v-slot:[`item.match_time`]="{ item }">
          <!--  if (item.is_validated & matchDate < currentTime & item.id !== localStorage.team_id) -->
          <v-tooltip v-if="!item.is_validated & (parseInt(item.home_team.id) === parseInt(team_id) || parseInt(item.away_team.id) === parseInt(team_id))" bottom>
            <template #activator="{ on }">
              <v-icon color="gray" class="mr-3" v-on="on">info</v-icon>
            </template>
            <span>Ottelu on validoimatta</span>
          </v-tooltip>
          <span>{{ item.match_time | moment('YYYY-MM-DD HH:mm') }}</span>
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
import moment from 'moment';

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
                { text: '', value: 'home_score_total', width:'3%', align: 'right'},
                { text: 'Tulos', value: 'dash', width:'1%', sortable: false, align: 'center'},
                { text: '', value: 'away_score_total', width:'3%', align: 'left'}
            ],
            data: [],
            matches: [],
            post_season: [],
            regular_season: [],
            team_id: '',
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
          let url = 'api/matches/?season='+sessionStorage.season_id;
          let i = 0;

          this.$http.get(url).then(
              function(data) {
                  this.data = data.body;
                  this.matches = data.body;

                  for (let object in data.body) {
                    // This is spaghetti to add a - to the column between scores.
                    data.body[i].dash = '-';

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
        },
        itemRowBackground: function(item) {
          // Handles the backround color of row items
          var matchDate = moment(item.match_time).format("YYYY-MM-DD HH:MM")
          var currentTime = moment(Date.now()).format("YYYY-MM-DD HH:MM")

          if (!this.team_id) return

          if (!item.is_validated & matchDate < currentTime & (parseInt(item.home_team.id) === parseInt(this.team_id) || parseInt(item.away_team.id) === parseInt(this.team_id))) return 'style-1'

          return 'style-2'
        }
    },
    mounted: function() {
        if (localStorage.team_id) {
          this.team_id = localStorage.team_id;
        } else {
          this.team_id = '';
        }
        
        this.getMatches();
    }
};
</script>
<style>
.style-1 {
  background-color: rgba(195, 20, 20, 0.781) !important;
}

.style-2 {
  background-color: white;
}

</style>

