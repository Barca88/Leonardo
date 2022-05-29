<template>
  <v-container fluid v-bind:style="{ backgroundColor: background_color }" v-if="1==1">
    <v-container v-if="dialog_statistics" class="d-flex justify-center" style="position: absolute; z-index: 9">
      <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
        <ModalLayout :desc="'Estatísticas'" :symbol="'mdi-chart-bar'" :buttonCode="'7.1'" v-on:quit="dialog_statistics = false"/>
      </vue-draggable-resizable>
    </v-container>
    <v-container v-if="dialog_rules" class="d-flex justify-center" style="position: absolute; z-index: 9">
      <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
        <ModalLayout :desc="'Regras'" :symbol="'mdi-ruler'" :buttonCode="'6.1'" v-on:quit="dialog_rules = false"/>
      </vue-draggable-resizable>
    </v-container>
    <v-container v-if="dialog_help" class="d-flex justify-center" style="position: absolute; z-index: 9">
      <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
        <ModalLayout :desc="'Ajuda'" :symbol="'mdi-lightbulb'" :buttonCode="'1.2'" v-on:quit="dialog_help = false"/>
      </vue-draggable-resizable>
    </v-container>
    <v-container v-if="dialog_about" class="d-flex justify-center" style="position: absolute; z-index: 9">
      <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
        <ModalLayout :desc="'Acerca'" :symbol="'fa fa-info-circle'" :buttonCode="'2.3'" v-on:quit="dialog_about = false"/>
      </vue-draggable-resizable>
    </v-container>
    <v-card-title style="font-size: 2em" class="mt-8">Domínio</v-card-title>
    <v-card-subtitle>{{ this.info.domain }}</v-card-subtitle>
    <v-card-title style="font-size: 2em">Subdomínios</v-card-title>
    <v-alert v-model="alert" dismissible type="error">
      Por favor, selecione pelo menos uma opção
    </v-alert>
    <v-spacer> </v-spacer>
    <v-card class="ma">
      <v-card-text>
          <v-list v-for="subdominio in subdomains" :key="subdominio.descricao">
            <div class="pretty p-default p-round p-thick">
              <input type="checkbox" :value="subdominio.descricao" v-model="subd_selected">
              <div class="state p-success-o">
                <label>{{subdominio.descricao}}</label>
              </div>
            </div>
          </v-list>
      </v-card-text>
    </v-card>
    <v-row class="ma-0" cols="12" flat v-bind:style="{ backgroundColor: background_color }" style="display: flex; justify-content: space-between">
        <v-col cols="6">
          <v-row style="height: 150px; float: left">
            <v-card class="ml-0" flat v-bind:style="{ backgroundColor: background_color }">
              <div>
                  <v-btn text disabled></v-btn>
              </div>
              <div class="mt-2">
                  <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="red" @click="verify_subDomain('evaluation')" v-bind="attrs" v-on="on">
                        <v-icon>mdi-lead-pencil</v-icon>
                      </v-btn>
                    </template>
                    <span>Avaliar</span>
                  </v-tooltip>
              </div>
              <div class="mt-2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#00cc99" @click="reload_component()" v-bind="attrs" v-on="on">
                        <v-icon>mdi-broom</v-icon>
                      </v-btn>
                    </template>
                    <span>Limpar</span>
                  </v-tooltip>
              </div>
            </v-card>
            <v-card class="ml-2" flat v-bind:style="{ backgroundColor: background_color }">
              <div>
                <v-btn text disabled></v-btn>
              </div>
              <div class="mt-2">
                  <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="red" @click="verify_subDomain('study')" v-bind="attrs" v-on="on">
                        <v-icon>mdi-book-open-page-variant</v-icon>
                      </v-btn>
                    </template>
                    <span>Estudar</span>
                  </v-tooltip>
              </div>
              <div class="mt-2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#00cc99" @click="change_component()" v-bind="attrs" v-on="on">
                        <v-icon>mdi-arrange-send-backward</v-icon>
                      </v-btn>
                    </template>
                    <span>Domínios</span>
                  </v-tooltip>
              </div>
            </v-card>
            <v-card class="ml-2" flat v-bind:style="{ backgroundColor: background_color }">
              <div>
                <v-btn text disabled></v-btn>
              </div>
              <div class="mt-2">
                <v-btn text disabled></v-btn>
              </div>
              <div class="mt-2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize"  color="#00cc99" @click="change_component()" v-bind="attrs" v-on="on">
                        <v-icon>mdi-flag-checkered</v-icon>
                      </v-btn>
                    </template>
                    <span>Terminar</span>
                  </v-tooltip>
              </div>
            </v-card>
          </v-row>
        </v-col>
        <v-col cols="6">
          <v-row style="height: 150px; float: right">
            <v-card class="mr-2" flat v-bind:style="{ backgroundColor: background_color }">
              <div >
                  <v-btn text disabled></v-btn>
              </div>
              <div class="mt-2">
                  <v-btn text disabled></v-btn>
              </div>
              <div class="mt-2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on" @click="dialog_rules = !dialog_rules">
                        <v-icon>mdi-ruler</v-icon>
                      </v-btn>
                    </template>
                    <span>Regras</span>
                  </v-tooltip>
              </div>
            </v-card>
            <v-card class="mr-2" flat v-bind:style="{ backgroundColor: background_color }">
              <div>
                  <v-btn text disabled></v-btn>
              </div>
              <div class="mt-2">
                  <v-tooltip left>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on">
                        <v-icon>mdi-volume-high</v-icon>
                      </v-btn>
                    </template>
                    <span>Voz</span>
                  </v-tooltip>
              </div>
              <div class="mt-2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on" @click="dialog_help = !dialog_help">
                        <v-icon>mdi-lightbulb</v-icon>
                      </v-btn>
                    </template>
                    <span>Ajuda</span>
                  </v-tooltip>
              </div>
            </v-card>
            <v-card class="mr-0" flat v-bind:style="{ backgroundColor: background_color }">
              <div>
                  <v-tooltip left>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on" @click="dialog_statistics = !dialog_statistics">
                        <v-icon>mdi-chart-bar</v-icon>
                      </v-btn>
                    </template>
                    <span>Estatísticas</span>
                  </v-tooltip>
              </div>
              <div class="mt-2">
                  <v-tooltip left>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on">
                        <v-avatar size="32">
                          <v-img :src="require('../assets/raccoon.png')">
                          </v-img>
                        </v-avatar>
                      </v-btn>
                    </template>
                    <span>Leonardo</span>
                  </v-tooltip>
              </div>
              <div class="mt-2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on" @click="dialog_about = !dialog_about">
                        <i class="fa fa-info-circle" style="font-size: 22px"></i>
                      </v-btn>
                    </template>
                    <span>Acerca</span>
                  </v-tooltip> 
              </div>
            </v-card>
          </v-row>
        </v-col>
    </v-row>
  </v-container>
  <Question v-else/>
</template>

<script>
  require('@/assets/styles/pretty-checkbox.min.css')
  import ModalLayout from './Modal_layout';

  export default {
    name: 'Subdomains_select',

    props: ['info'],

    components: {
      ModalLayout
    },

    data() {
        return {
          background_color: "#F7F7F7", alert: false, subd_selected: [], type_of_session: "", subdomains: [],
          dialog_statistics: false, dialog_rules: false, dialog_help: false, dialog_about: false
        }
      },
    created(){
      this.info.subdomains.forEach(element => { this.subdomains.push({ descricao: element }) })
      this.subdomains.push({ descricao: "Todos" })
    },
    methods: {
      async verify_subDomain(type_of_session){
        if(this.subd_selected.length == 0) this.alert = true 
        else{
          var subdomains_to_send = []

          this.type_of_session = type_of_session
          if(this.subd_selected.includes("Todos")){
            var keep_all_subdomains = this.subdomains

            keep_all_subdomains.forEach(element => { if(element != "Todos") subdomains_to_send.push(element) })
          }
          else{ this.subd_selected.forEach(element => { subdomains_to_send.push(element) }) }
          var quizz_parameters = {
            domain: this.info.domain,
            subdomains: JSON.stringify(subdomains_to_send),
            id: this.info.id,
            username: this.info.username,
            name: this.info.name,
            email: this.info.email,
            gender: this.info.gender,
            degree: this.info.degree,
            user_type: this.info.user_type,
            session_mode: this.type_of_session
          }

          await this.$store.commit('set_quizz_parameters', quizz_parameters)

          window.open('http://localhost:8080/quizz', "", 'width=1000,height=800,scrollbars=no,resizable=no')
        }
      },
      reload_component(){
        this.subd_selected = []
        this.alert = false
      },
      change_component(){ this.$emit("showDomainsSelectPage"); }
    },
  }
</script>
