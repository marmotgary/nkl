<template>
  <v-card>
    <v-card-title>Ottelut
      <v-spacer></v-spacer>
      <v-text-field v-model="search" label="Search" single-line hide-details></v-text-field>
    </v-card-title>
    <v-data-table :headers="headers" :items="matches" :search="search" hide-actions>
      <template slot="headers" class="text-xs-center"></template>
      <template slot="items" slot-scope="props">
        <td>{{ props.item.aika }}</td>
        <td class="text-xs-left">{{ props.item.koti }}</td>
        <td class="text-xs-left">{{ props.item.vieras }}</td>
        <td class="text-xs-left">{{ props.item.tulos }}</td>
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
                    text: 'Aika',
                    align: 'left',
                    value: 'aika'
                },
                { text: 'Koti', value: 'koti' },
                { text: 'Vieras', value: 'vieras' },
                { text: 'Tulos', value: 'tulos' }
            ],
            matches: [
                {
                    aika: '01-23-2019 20:00',
                    koti: 'Nöhö',
                    vieras: 'Anaheim',
                    tulos: '34-5'
                },
                {
                    aika: '01-23-2019 20:00',
                    koti: 'Darts',
                    vieras: 'CLG',
                    tulos: '32-43'
                },
                {
                    aika: '01-23-2019 20:00',
                    koti: 'KKK',
                    vieras: 'SFS',
                    tulos: '54-34'
                },
                {
                    aika: '01-23-2019 19:30',
                    koti: 'kW',
                    vieras: 'Nöhö',
                    tulos: '123-43'
                },
                {
                    aika: '01-23-2019 19:30',
                    koti: 'Sick',
                    vieras: 'Darts',
                    tulos: '12-3'
                },
                {
                    aika: '01-23-2019 19:30',
                    koti: 'KKK',
                    vieras: 'Sick',
                    tulos: '30-44'
                },
                {
                    aika: '01-23-2019 19:00',
                    koti: 'Nöhö',
                    vieras: 'Darts',
                    tulos: '20-20'
                },
                {
                    aika: '01-23-2019 19:00',
                    koti: 'Draco',
                    vieras: 'SFS',
                    tulos: '22'
                }
            ]
        };
    }
};
</script>
