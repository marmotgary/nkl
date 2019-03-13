

<template>
  <v-card>
    <v-card-title>Joukkueet
      <v-spacer></v-spacer>
    </v-card-title>
    <div class="single-team"></div>
    <!-- <v-data-table :headers="headers" :items="teams" hide-actions>
      <template slot="headers" class="text-xs-left"></template>
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td class="text-xs-left">{{ props.item.ottelut }}</td>
        <td class="text-xs-left">{{ props.item.voitot }}</td>
        <td class="text-xs-left">{{ props.item.tasapelit }}</td>
        <td class="text-xs-left">{{ props.item.häviöt }}</td>
        <td class="text-xs-left">{{ props.item.pisteet }}</td>
        <td class="text-xs-left">{{ props.item.piste_ero }}</td>
        <td class="text-xs-left"></td>
      </template>
    </v-data-table>-->
  </v-card>
</template>

<script>
export default {
    data() {
        return {};
    },
    methods: {},
    created() {
        this.$http.get('http://localhost:8000/api/teams/').then(function(data) {
            console.log(data);
        });
    }
};
</script>
