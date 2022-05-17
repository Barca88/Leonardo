<template>
    <v-app>
  <div>
    <div>
      <!-- Adicionar template v-slot:top -->
      <template>
        <v-toolbar flat color="white">
          <v-toolbar-title>Verificação de Questões</v-toolbar-title>
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
            <v-btn
              color="#03254c"
              v-on:click="aproveSelected()"
              class="im-btn"
              dark
            >
              <v-icon>mdi-sticker-check-outline</v-icon>
            </v-btn>

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
        :items="questions"
        :items-per-page="5"
        :search="search"
        multi-sort
      >
        <template v-slot:item.flag="{ item }">
          <v-icon small :color="getColor(item.flag)"> mdi-flag </v-icon>
        </template>

        <template v-slot:item.actions="{ item }">

        <v-btn id="eye" icon @click="eyeClick(item,questions.indexOf(item))">
          <v-icon medium class="mr-2">
            mdi-eye
          </v-icon>
        </v-btn> 

        <v-icon medium color="#4CAF50" @click="confirmDialog(item, 'aprove')">
            mdi-checkbox-marked-circle
          </v-icon>

          <router-link :to="{ name: 'ProdQuestao', params: { question: item } }">
            <v-icon  medium class="mr-2">
            mdi-pencil
          </v-icon>       
          </router-link>
               
          <v-icon medium @click="confirmDialog(item, 'reject')">
            mdi-trash-can-outline
          </v-icon>
          <p-check
            class="p-default p-round p-thick"
            color="primary-o"
            v-model="selected"
            :value="item"
          ></p-check>
        </template>
      </v-data-table>
    </div>

</div>
<Carousel :alertPopup="alertPopup" :questions="questions" :index="index" v-if="carousel_display"/>

<GenericAlert :alertPopup="alertPopup" ref="popup"/>
</v-app>

</template>

<script>
import axios from "axios";
import helpers from "../../../public/scripts/helpers.js"
import Carousel from "../../components/Importacao/Carousel.vue"
import GenericAlert from '../../components/Importacao/GenericAlert.vue'

export default {
    metaInfo:{
      title:'Leonardo-Verificação de Questões'
    },
    components: {
      Carousel, GenericAlert
    },
  data() {
    return {
        carousel_display: false,
        index : null,
        dialog: false,
        currentQuestion: {},
        alertPopup: {},
      headers: [
        {
          text: "E",
          value: "flag",
        },
        {
          text: "Identificador",
          value: "_id",
          align: "align-content-start",
          sortable: true,
          class: "white--text",
        },
        {
          text: "Domínio",
          value: "domain",
          align: "align-content-start",
          sortable: true,
          class: "white--text",
        },
        {
          text: "SubDomínio",
          value: "subdomain",
          align: "align-content-start",
          class: "white--text",
        },
        {
          text: "Autor",
          value: "author",
          align: "align-content-start",
          class: "white--text",
        },
        {
          text: "Data Criação",
          value: "inserted_at",
          align: "align-content-start",
          class: "white--text",
        },
        {
          text: "Opções",
          value: "actions",
          sortable: false,
        },
      ],
      questions: [],
      selected: [],
      search: "",
      identificador: "",
    };
  },
  created() {
    this.loadQuestions();
  },
  methods: {
    eyeClick (question,index) {
        this.carousel_display = !this.carousel_display;
        this.index = index
    },

    loadQuestions: function () {
      axios.get(`${process.env.VUE_APP_BACKEND}/importation/imported_questions?nome=${this.$store.state.user._id}`,{},{
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"       
          }}
        ).then((resp) => {
        this.questions = resp.data.questions;
      });
    },
    async confirmDialog (item, str) {

        helpers.confirmDialog(item, str, this.$refs.popup)
    },

    aproveQuestion: helpers.aproveQuestion,

    rejectQuestion: helpers.rejectQuestion,

    editQuestion: helpers.editQuestion,

    getColor: function (flag) {
      if (flag === "aproved") return "#00E676";
      else if (flag === "rejected") return "#F44336";
      else return "#2196F3";
    },

    aproveSelected: function () {
      let aproved = [], invalid = []
      this.selected.forEach((question) => {
        if (question.flag === "aproved") {
          aproved.push(question.id);
        } else if (question.flag === "rejected") {
          invalid.push(question.id);
        } else {
          question.flag = "aproved";
          axios.put(`${process.env.VUE_APP_BACKEND}/importation/imported_questions/` + question.id + `?nome=${this.$store.state.user._id}`,question,{
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer: ${this.$store.state.jwt}`,
              'Access-Control-Allow-Origin': "*"       
            }}
          );
        }
      });
      if (aproved.length > 0 || invalid.length > 0) {
        alert(
          "Failed to add\nAlready Aproved:\n" + aproved + "\nInvalid questions:\n" + invalid + "\n"
        );
      }
      this.selected = [];
    },
  },
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
  font-family: "Roboto";
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
