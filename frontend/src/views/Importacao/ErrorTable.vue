<template>
    <v-app>
  <div>
      <appHeader :ajuda='ajuda'></appHeader>
      <navDraw></navDraw>
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
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
            <v-btn color="#2A3F54" dark class="mb-2" @click="dialog = true" v-on="{ ...tooltip}">
                <v-icon>mdi-trash-can</v-icon>
            </v-btn>
            </template>
            <span>
                {{$t('hist.cleanH')}}
            </span>
          </v-tooltip>
          <div id="btn-group">
            <v-btn color="#03254c" v-print="'#printMe'" class="im-btn" dark>
              <v-icon>mdi-printer</v-icon>
            </v-btn>
          </div>
          <v-dialog
        v-model="dialog"
        scrollable 
        width="500"
        persistent
    >
        <v-card>
            <v-toolbar color="#2A3F54" dark>
                <h1>{{$t('hist.haccess')}}</h1>
            </v-toolbar>
            <v-row>
            <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
            </v-col>
            <v-col>
                <v-card-text>
                <h3>{{$t('hist.elim')}}</h3>
                </v-card-text>
            </v-col>
            </v-row>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                    <v-btn @click="dialog = false;eliminarHistorico()" v-on="{ ...tooltip}" class="mr-5">
                        <v-icon>mdi-check</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{$t('navd.confirm')}}
                    </span>
                </v-tooltip>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                    <v-btn @click="dialog = false" v-on="{ ...tooltip}">
                        <v-icon>mdi-exit-to-app</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{$t('navd.nao')}}
                    </span>
                </v-tooltip>
            </v-card-actions>
        </v-card>
    </v-dialog>
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
import Header from '../../components/header.vue'
import NavDraw from '../../components/navDraw.vue'
import alerts from "../../../public/scripts/alerts.js"
import GenericAlert from '../../components/Importacao/GenericAlert.vue'

export default {
    metaInfo:{
      title:'Leonardo-Verificação de Erros'
    },

    components:{
        GenericAlert,
        'appHeader': Header,
        'navDraw':NavDraw
    },
  data() {
    return {
        alertPopup: {},
        dialog:false,
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
        if(popup.type === "confirm") this.alertPopup = alerts.confirmDialog(popup.message,null)
        else if(popup.type === "info") this.alertPopup = alerts.infoDialog(popup.message,null)
        else if(popup.type === "del") this.alertPopup = alerts.errorDialog(popup.message,null) // error
        else if(popup.type === "warn") this.alertPopup = alerts.warningDialog(popup.message,null)
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

    eliminarHistorico:function(){
      axios.get(`${process.env.VUE_APP_BACKEND}/importation/errorCleanse?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
      .then(response => {
          console.log(response)
          this.errors=response.data.history

      }).catch(e => {
          console.log(e)
      })
      }
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
