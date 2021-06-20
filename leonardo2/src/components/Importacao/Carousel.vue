<template v-slot:activator="{ on, attrs }">
  <v-app class="carousel-box" id="inspire">
    <v-row justify="center">
      <v-dialog
        persistent
        v-model="dialog"
        transition="dialog-bottom-transition"
        @keydown.esc="close()"
      >
              <!-- fullscreen  inside v-dialog -->

        <v-card
        color="#4B779E"
        >
          <v-row  align="start">
                    <v-col class="shrink">
                         <v-img src="@/assets/LeonardoLogo.png" height="75" max-width="80" class="ml-3"></v-img>
                    </v-col>
                    <v-col>
                         <v-card-title class="fst-heading" >Produção</v-card-title>
                         <v-card-subtitle class="snd-heading">Verificação de Questões</v-card-subtitle>
                     </v-col>
          </v-row>

          <v-list three-line subheader>
            <v-carousel
              max-width="50%"
              show-arrows-on-hover
              hide-delimiters
              :show-arrows="true"
            >
              <v-carousel-item v-for="(question,i) in this.questionsShuffled" :key="i">
                <v-sheet :color="color" >

                  <v-row class="fill-height" align="center" justify="center">
                    <div class="display-3">
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              class="label-style"
                              label="Flag"
                              value=""
                              readonly
                              required
                              >
                              <template slot="append">
                                <v-icon small :color="getColor(question.flag)"> mdi-flag </v-icon>
                              </template>
                              </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="" md="4">
                            <v-text-field
                              label="Identificador"
                              class="label-style"
                              readonly
                              v-model="question.identifier"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              class="label-style"
                              label="Domínio"
                              readonly
                              v-model="question.domain"
                              required
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              class="label-style"
                              label="Sub-Domínio"
                              readonly
                              v-model="question.subdomain"
                              required
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              class="label-style"
                              label="Data de criação"
                              readonly
                              v-model="question.inserted_at"
                              required
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              class="label-style"
                              label="Autores"
                              readonly
                              v-model="question.author"
                              required
                            ></v-text-field>
                          </v-col>
                          <div style="margin: auto">
                            <v-btn  class="btn-carousel"  color="warning" @click="confirmDialog(question, 'aprove')" >
                              <v-icon >mdi-sticker-check-outline</v-icon>
                            </v-btn>

                            <v-btn class="btn-carousel" color="primary" @click="editQuestion(question)">
                                <v-icon  medium > mdi-pencil</v-icon>
                            </v-btn>

                            <v-btn  class="btn-carousel" color="error" @click="confirmDialog(question, 'reject')">
                              <v-icon medium > mdi-trash-can-outline </v-icon>
                            </v-btn>
                          </div>


                        </v-row>
                      </v-container>
                    </div>
                  </v-row>
                </v-sheet>
              </v-carousel-item>
            </v-carousel>
          </v-list>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="#16207f" v-on:click="help()" class="im-btn" dark>
                    <v-icon>mdi-help</v-icon>
            </v-btn>

              <v-btn color="#00E676" v-on:click="close()" class="im-btn" dark>
                    <v-icon>mdi-door-open</v-icon>
            </v-btn>
              <GenericAlert :alertPopup="alertPopup" ref="popup"/>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-app>
</template>


<script>
import helpers from "../../../public/scripts/helpers.js";
import alerts from "../../../public/scripts/alerts.js"
import GenericAlert from './GenericAlert.vue'

export default {
  name: "Table",
  props: ["questions", "index"],
  data() {
    return {
      dialog: true,
      color: "white",
      i: this.index,
      questionsShuffled:[],
      alertPopup: {},
      image:"@/assets/LeonardoLogo.png"
    };
  },
   components:{
        GenericAlert
    },

  methods: {
   shuffleArray: function(index) {
       var copiedQuestions = this.$props.questions.map((x)=>x);
       var half =  copiedQuestions.splice(index);
       this.questionsShuffled= half.concat(copiedQuestions);
  },


    async confirmDialog (item, str) {
        helpers.confirmDialog(item, str, this.$refs.popup)
    },

    getColor: function (flag) {
      if (flag === "aproved") return "#00E676";
      else if (flag === "rejected") return "#F44336";
      else return "#2196F3";
    },

    aproveQuestion: helpers.aproveQuestion,

    rejectQuestion: helpers.rejectQuestion,

    editQuestion: helpers.editQuestion,

    async close() {
      this.dialog = false;
      await new Promise(r => setTimeout(r, 10))
      document.getElementById("eye").click();
    },
     help: function(){
        this.alertPopup=alerts.infoDialog("Alguma informação relevante para o utilizador.<br> Algum texto nesta linha.")
        }
  },
  mounted: function () {
    this.$nextTick(function () {
      // Code that will run only after the
      // entire view has been rendered
      document.getElementsByClassName("v-carousel__controls__item")[this.index].click();
    });
  },
  created: function(){
    this.shuffleArray(this.i);
  }


};
</script>


<style >


.btn-carousel {
  margin: 25px;
}


.v-carousel{
  height: 350px !important;
}

.theme--dark.v-input input{
  color: black !important;
  font-family: "Roboto";
  font-size: 20px !important;

}

.theme--dark.v-label{

color: gray !important;
font-family: "Roboto";
font-size: 20px !important;

}

.theme--dark.v-messages{
    color:rgb(53, 53, 53) !important;

}

/* Cor associada a linha sobre o texto depois de selecionada. */
.v-text-field .v-input__control {
  color:black !impotant;
}

div.v-input__slot::before{
  background-color: black;
}

i.v-icon.notranslate.mdi.mdi-circle.theme--dark{
    color: gray;
}

.fst-heading{
  color: yellow;
  font-family: "Roboto";
  font-weight: bold;
  font-size: 30px ;
}

.snd-heading{
   color: white  !important;
  font-family: "Roboto";
  font-size: 30px ;
  font-weight: bold;
  margin-top: -2px !important;

}

.display-3{
  margin-bottom: 0px;
  margin-top: 20px;

}
</style>
