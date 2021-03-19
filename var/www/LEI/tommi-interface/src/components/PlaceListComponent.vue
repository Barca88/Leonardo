<template>
    <div>
      <v-dialog v-model="showConfirm" persistent lazy absolute max-width="400">
        <v-card>
          <v-card-title class="headline">Deseja Remover {{ place.nome }} ?</v-card-title>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red darken-1" rounded @click="removeLocalidade(place)">Sim</v-btn>
            <v-btn color="blue darken-1" rounded @click="showConfirm = false">Não</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <div>
        <v-data-table :headers="headers" :items="places" :search="search" :items-per-page="15" :sort-by="['id']" :sort-desc="[true,true,true,true,false]" multi-sort>
          <template v-slot:top>
            <v-toolbar flat color="white">
              <v-toolbar-title><b>Localidades</b></v-toolbar-title>
                    <v-divider
                    class="mx-4"
                    inset
                    vertical
                    ></v-divider>
                    <v-spacer></v-spacer>
                    <v-text-field
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Procura"
                      single-line
                      hide-details
                      class="mr-5"
                    ></v-text-field>
                </v-toolbar>
          </template>
          <template v-slot:header.nome="{ header }" >
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.latitude="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.longitude="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.nFolios="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.opcao="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:item.opcao="{ item }">
                <v-icon
                    small
                    class="mr-2"
                    @click="goMap(item)"
                >
                    mdi-eye
                </v-icon>
                <v-icon
                    small
                    @click.stop="openDialog(item)"
                >
                    mdi-trash-can
                </v-icon>
            </template>
        </v-data-table>
      </div>
    </div>
</template>
<script>
import axios from 'axios'
const lhost = 'https://tommi2.di.uminho.pt/api/'
export default {
  data () {
    return {
      search: '',
      headers: [
        {
          text: 'Nome',
          align: 'start',
          value: 'nome'
        },
        { text: 'Latitude', value: 'latitude' },
        { text: 'Longitude', value: 'longitude' },
        { text: 'NFólios', value: 'nFolios' },
        { text: 'Opções', sortable: false, value: 'opcao' }
      ],
      places: [],
      showConfirm: false,
      place: {}
    }
  },
  mounted: async function () {
    try {
      var response = await axios.get(lhost + 'getPlaces',{headers: { 'Authorization': `Bearer: ${this.$store.state.jwt}`}})
      this.places = response.data
    } catch (e) {
      return e
    }
  },
  methods: {
    goMap: function (item) {
      this.$router.push({
        path: '/admin/localidades/' + item.nome,
        query: {
          nome: item.nome,
          latitude: item.latitude,
          longitude: item.longitude
        }
      })
    },
    openDialog: function (item) {
      this.place = item
      this.showConfirm = true
    },
    removeLocalidade: async function (item) {
      try {
        await axios.post(lhost + 'remove', item, {headers: { 'Authorization': `Bearer: ${this.$store.state.jwt}`}})
        this.places.splice(item, 1)
        this.showConfirm = false
      } catch (e) {
        return e
      }
    }
  }
}
</script>
<style scoped>
    /* .tommitable .v-data-table .table{ */
   .v-data-table /deep/ th{
        background-color:#4b779e;
    }
    .v-data-table /deep/ tr{
        color: #73879C;
        font-size: 13px;
    }
    .v-data-table /deep/ tr:nth-child(even){
        background-color: lightgray;
    }
    #folios *{
            box-sizing: border-box;
    }
    #folios{
            margin: 20px auto;
            max-width: 1100px;
            margin-bottom: 80px;
    }
    label {
        color: white;
        padding: 8px;
        font-family: Arial, sans-serif;
        font-weight: bold;
        font-size: 15px;
    }
    b{
        font-size: 14px;
    }
</style>
