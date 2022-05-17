<template>
    <v-app>
  <div>
    <div>
      <!-- Adicionar template v-slot:top -->
      <template>
        <v-toolbar flat color="white">
          <v-toolbar-title>Verificação de Erros</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <!-- Barra de Pesquisa -->
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            :label="$t('title.pesq')"
            single-line
            hide-details
            class="mr-5 search-bar"
          ></v-text-field>
          <div id="btn-group">
            <v-btn color="#03254c" v-print="'#printMe'" class="im-btn" dark>
              <v-icon>mdi-printer</v-icon>
            </v-btn>
          </div>
        </v-toolbar>
      </template>
    </div>

    <div id="printMe">
      <v-data-table
        :headers="headers"
        :items="errors"
        :items-per-page="15"
        :search="search"
        multi-sort
      >

        <template v-slot:item.actions="{ item }">
        <v-btn id="eye" icon @click="eyeClick(item)"> <v-icon medium class="mr-2"> mdi-eye </v-icon> </v-btn>
        </template>
      </v-data-table>
    </div>

</div>
    <GenericAlert :alertPopup="alertPopup" ref="popup"/>
</v-app>
</template>

<script>
import moment from 'moment'
import axios from "axios";
import alerts from "../../../public/scripts/alerts.js"
import helpers from "../../../public/scripts/helpers.js"
import GenericAlert from '../../components/Importacao/GenericAlert.vue'

export default {
    metaInfo:{
      title:'Leonardo-Verificação de Erros'
    },

    components:{
        GenericAlert
    },
  data() {
    return {
        alertPopup: {},
      headers: [
        {
          text: "Identificador",
          value: "id",
          align: "align-content-start",
          sortable: true,
          class: "white--text",
        },
        {
          text: "Header",
          value: "header",
        },
        {
          text: "Tipo",
          value: "type",
          align: "align-content-start",
          sortable: true,
          class: "white--text",
        },       {
          text: "Data Criação",
          value: "createdAt",
          align: "align-content-start",
          class: "white--text",
        },
        {
          text: "Opções",
          value: "actions",
          sortable: false,
        }
      ],
      errors: [],
      search: "",
    };
  },
  created() {
    this.loadErrors();
  },
  methods: {
    async eyeClick (popup) {
        if(popup.type === "confirm") this.alertPopup = alerts.confirmDialog(popup.message)
        else if(popup.type === "info") this.alertPopup = alerts.infoDialog(popup.message)
        else if(popup.type === "del") this.alertPopup = alerts.errorDialog(popup.message) // error
        else if(popup.type === "warn") this.alertPopup = alerts.warningDialog(popup.message)
    },
    async confirmDialog (item) {
        helpers.confirmDialog(item, this.$refs.popup)
    },
    formatDate: function (d) {
        return moment(d).format("YYYY-MM-DD hh:mm");
    },
    loadErrors: function () {
      axios.get(`${process.env.VUE_APP_BACKEND}/importation/imported_errors?nome=${this.$store.state.user._id}`,{},{
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"       
          }}
        ).then((resp) => {
        this.errors = resp.data.errors;
        this.errors.reverse();
        // Fix the date to a better format right here
        this.errors.forEach(obj => obj.createdAt = this.formatDate(obj.createdAt));
      });
    },
  }
};
</script>

<style scoped>
.v-data-table /deep/ th {
  background-color: #4b779e;
  color: white !important;
 font-size: 16px !important;
  font-weight: bolder !important;
}

.v-toolbar__title {
  font-size: 30px;
  font-family: "Roboto" ;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: bold;
}

.search-bar {
  margin-right: 25px;
}

.v-data-table /deep/ tr > td {
  color: black;
  font-family: "Roboto";
  font-size: 16px !important;

}

.v-data-table /deep/ tr:nth-child(even) {
  background-color: rgb(245, 245, 245);
}

.v-btn {
  margin-right: 10px;
}

.v-icon{
    margin-right: 5px;
}

#docs * {
  box-sizing: border-box;
}

#docs {
  margin: 20px auto;
  max-width: 1100px;
  margin-bottom: 80px;
}
</style>
