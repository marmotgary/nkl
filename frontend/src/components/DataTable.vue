<template>
  <v-card>
    <v-card-title>Joukkueet
      <v-spacer></v-spacer>
      <v-text-field v-model="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>
    <v-data-table :headers="headers" :items="teams" :search="search" hide-actions>
      <template slot="headers" class="text-xs-center"></template>
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
    data() {
        return {
            search: '',
            headers: [
                {
                    text: 'Joukkue',
                    align: 'left',
                    sortable: false,
                    value: 'name',
                    width: '1%'
                },
                { text: 'O', value: 'ottelut', width: '1%', align: 'left' },
                { text: 'V', value: 'voitot', width: '1%', align: 'left' },
                { text: 'T', value: 'tasapelit', width: '1%', align: 'left' },
                { text: 'H', value: 'häviöt', width: '1%', align: 'left' },
                { text: 'P', value: 'pisteet', width: '1%', align: 'left' },
                {
                    text: 'kPE',
                    value: 'piste_ero',
                    width: '1%',
                    align: 'left'
                },
                { align: 'left', text: '', value: 'name' }
            ],
            teams: [
                {
                    name: 'Nöhö',
                    ottelut: 16,
                    voitot: 14,
                    tasapelit: 0,
                    häviöt: 2,
                    pisteet: 28,
                    piste_ero: '-171'
                },
                {
                    name: 'Ehkä',
                    ottelut: 16,
                    voitot: 10,
                    tasapelit: 0,
                    häviöt: 6,
                    pisteet: 20,
                    piste_ero: -10
                },
                {
                    name: 'Darts',
                    ottelut: 16,
                    voitot: 4,
                    tasapelit: 0,
                    häviöt: 12,
                    pisteet: 8,
                    piste_ero: -8
                },
                {
                    name: 'CLG',
                    ottelut: 16,
                    voitot: 1,
                    tasapelit: 1,
                    häviöt: 14,
                    pisteet: 3,
                    piste_ero: -1
                },
                {
                    name: 'kyRSÄ',
                    ottelut: 16,
                    voitot: 0,
                    tasapelit: 0,
                    häviöt: 16,
                    pisteet: 0,
                    piste_ero: +50
                },
                {
                    name: 'HUI',
                    ottelut: 16,
                    voitot: 12,
                    tasapelit: 3,
                    häviöt: 1,
                    pisteet: 27,
                    piste_ero: -300
                },
                {
                    name: 'W(h)y',
                    ottelut: 16,
                    voitot: 8,
                    tasapelit: 0,
                    häviöt: 8,
                    pisteet: 16,
                    piste_ero: '-74'
                },
                {
                    name: 'KKK',
                    ottelut: 16,
                    voitot: 3,
                    tasapelit: 6,
                    häviöt: 7,
                    pisteet: 15,
                    piste_ero: -30
                }
            ]
        };
    }
};
</script>
