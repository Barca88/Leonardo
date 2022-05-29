<template>
    <v-container v-if="1==1">
        <div>
            <div>
                <h1>Avaliação - {{ this.selected_domain }}</h1>
            </div>
            <v-spacer></v-spacer>
            <v-container v-if="dialog_resume" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <Resume :statsObj="statistics_object" v-on:quit="dialog_resume = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_rules" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Regras'" :symbol="'mdi-ruler'" :buttonCode="'6.3'" v-on:quit="dialog_rules = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_help" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Ajuda'" :symbol="'mdi-lightbulb'" :buttonCode="'1.4'" v-on:quit="dialog_help = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_about" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Acerca'" :symbol="'fa fa-info-circle'" :buttonCode="'2.5'" v-on:quit="dialog_about = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-container v-if="dialog_statistics" class="d-flex justify-center" style="position: absolute; z-index: 9">
                <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
                    <ModalLayout :desc="'Estatísticas'" :symbol="'mdi-chart-bar'" :buttonCode="'7.3'" v-on:quit="dialog_statistics = false"/>
                </vue-draggable-resizable>
            </v-container>
            <v-card>
                <v-card-title> Está na hora de fazer uma pausa</v-card-title>
                <v-card-text> {{ message }} </v-card-text>
            </v-card>

            <v-row cols="12" style="display: flex; justify-content: space-between">
                <v-col cols="6">
                    <v-row style="height: 150px; float: left">
                        <v-card class="ml-3" flat>
                            <div>
                                <v-tooltip right>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn @click="dialog_resume = !dialog_resume" block class="white--text text-capitalize" color="red" v-bind="attrs" v-on="on"><v-icon>mdi-file-document</v-icon></v-btn>
                                    </template>
                                    <span>Resumo</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on" v-if="route == true"><v-icon>mdi-arrange-send-backward</v-icon></v-btn>
                                        <v-btn :to="{ name: 'dom'}" class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on" v-else><v-icon>mdi-arrange-send-backward</v-icon></v-btn>
                                    </template>
                                    <span>Domínios</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                        <v-card class="ml-2" flat>
                            <div>
                                <v-btn text disabled></v-btn>
                            </div>
                            <div class="mt-2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn 
                                            class="white--text text-capitalize" 
                                            color="#00cc99"
                                            @click="windowClose()"
                                            v-bind="attrs" v-on="on"
                                        > 
                                            <v-icon>mdi-door-open</v-icon>
                                        </v-btn>
                                    </template>
                                    <span>Sair</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                    </v-row>
                </v-col>
               <v-col cols="6">
                    <v-row style="height: 150px; float: right">
                        <v-card class="mr-2" flat>
                            <div>
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
                        <v-card class="mr-2" flat>
                            <div>
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn class="white--text text-capitalize" color="#172d44" @click="popupInquiry()" v-bind="attrs" v-on="on"><v-icon>mdi-comment-outline</v-icon></v-btn>
                                    </template>
                                    <span>Opinião</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn @click="dialog_help = !dialog_help" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-lightbulb</v-icon></v-btn>
                                    </template>
                                    <span>Ajuda</span>
                                </v-tooltip>
                            </div>
                        </v-card>
                        <v-card class="mr-3" flat>
                            <div> 
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn @click="dialog_statistics = !dialog_statistics" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on"><v-icon>mdi-chart-bar</v-icon></v-btn>
                                    </template>
                                    <span>Estatísticas</span>
                                </v-tooltip>
                            </div>
                            <div class="mt-2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn @click="dialog_about = !dialog_about" class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on">
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
        </div>
    </v-container>
    <Opinion v-else/>
</template>

<script>
  import ModalLayout from './Modal_layout';
  import Resume from './Resume';

  export default {
    name: 'Break',

    components: {
        ModalLayout, Resume
    },

    props: ['message'],

    data: function () {
        return {
            route: true, dialog_resume: false, dialog_opinion: false, dialog_statistics: false, dialog_rules: false, dialog_help: false, dialog_about: false, on: "", selected_domain: this.$store.getters.get_quizz_parameters.domain, statistics_object: {}
        }
    },
    async created() {
        this.route = true
        var user = await this.$store.getters.get_session_user
        
        this.$http.get('https://leonardo.di.uminho.pt/api/v0/evaluation/getStatistics?userName=' + user.username)
        .then(response => {
            this.statistics_object = JSON.parse(response.data)
        })
        .catch(error => {
            throw(error)
        })
    },
    methods: {
      windowClose(){ window.close(); },
      async popupInquiry() {
        await this.$store.commit('set_inquiry_id', 'PTSEFS01')
        window.open('https://leonardo.di.uminho.pt/evaluation/inquiry', '_blank', 'width=615, height=500');
      }
    }
  }
</script>
