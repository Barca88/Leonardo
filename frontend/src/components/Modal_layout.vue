<template>
    <v-card style="border-radius:0px; height: 250px">
        <v-app-bar color="#172d44" dark>
            <div class="d-flex align-center">
                <h3 width="40" v-if="(desc == 'Sair da sessão') || (desc == 'Sem resposta')"> Aviso </h3>
                <h3 width="40" v-else> {{ desc }} </h3>
            </div>
        </v-app-bar>
        <v-container>
            <div style="height: 110px;">
                <v-row cols="12">
                    <v-col cols="2">
                        <v-row>
                            <v-card class="ml-4 mt-1" color="red" flat height="65px" width="70px" v-if="(desc == 'Sair da sessão') || (desc == 'Sem resposta')">
                                <div>
                                    <v-icon v-bind:style="'border: 0px solid red; color: white; border-radius:0%; size: 30; height: 65px; width: 70px;'">{{ symbol }}</v-icon>
                                </div>
                            </v-card>
                            <v-card class="ml-4 mt-1" color="#172d44" flat height="65px" width="70px" v-else>
                                <div style="text-align: center;" v-if="(desc != 'Acerca') && (desc != 'Acerca de') && (desc != 'Créditos') && (desc != 'Termos de utilização') && (desc != 'Privacidade')">
                                    <v-icon v-bind:style="'border: 0px #172d44; color: white; border-radius:0%; size: 30; height: 65px; width: 70px;'">
                                        {{ symbol }}
                                    </v-icon>
                                </div>
                                <div style="text-align: center; margin-top: 18px" v-else>
                                    <i v-bind:class="symbol" style="border: 0px #172d44; color: white; border-radius:0%; font-size: 22px"></i>
                                </div>
                            </v-card>
                        </v-row>
                    </v-col>
                    <v-col cols="10">
                        <v-row>
                            <v-card class="mr-4" flat>
                                <vue-custom-scrollbar class="scroll-area" :settings="settings"  v-if="(desc == 'Sair da sessão') || (desc == 'Sem resposta') || (desc == 'Gamificação')">
                                    <v-card-text style="font-size: 15px;">{{ text }}</v-card-text>
                                </vue-custom-scrollbar>
                                <vue-custom-scrollbar class="scroll-area" :settings="settings" v-else>
                                    <v-card-text style="font-size: 15px;">{{ modal_text }}</v-card-text>
                                </vue-custom-scrollbar>
                            </v-card>
                        </v-row>
                    </v-col>
                </v-row>
            </div>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                    <v-btn class="white--text text-capitalize; mr-2" color="#e6b800" @click="answer()" v-if="(desc == 'Sem resposta')" v-bind="attrs" v-on="on"><v-icon>mdi-checkbox-marked-outline</v-icon></v-btn>
                    </template>
                    <span>Responder</span>
                </v-tooltip>
                <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                    <v-btn class="white--text text-capitalize; mr-2" color="#00cc99" @click="next()" v-if="(desc == 'Sem resposta')" v-bind="attrs" v-on="on"><v-icon>mdi-chevron-double-right</v-icon></v-btn>
                    </template>
                    <span>Próxima questão</span>
                </v-tooltip>
                <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                    <v-btn class="white--text text-capitalize; mr-2" color="#00cc99" @click="cancel()" v-if="(desc == 'Sair da sessão')" v-bind="attrs" v-on="on"><v-icon>mdi-cancel</v-icon></v-btn>
                    </template>
                    <span>Cancelar</span>
                </v-tooltip>
                <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                    <v-btn class="white--text text-capitalize; mr-3;" color="#00cc99" @click="quit()" v-if="(desc != 'Acerca de') && (desc != 'Créditos') && (desc != 'Termos de utilização') && (desc != 'Privacidade')" v-bind="attrs" v-on="on"><v-icon>mdi-door-open</v-icon></v-btn>
                    </template>
                    <span>Sair</span>
                </v-tooltip>
            </v-card-actions>
        </v-container>
    </v-card>
</template>

<script>
  import vueCustomScrollbar from 'vue-custom-scrollbar'
  import "vue-custom-scrollbar/dist/vueScrollbar.css"
  export default {
    name: 'Modal_layout',

    props: ['desc', 'symbol', 'buttonCode', 'text'],

    components: {
        vueCustomScrollbar
    },

    data: function () {
        return {
            modal_text: "",
            settings: {
                suppressScrollY: false,
                suppressScrollX: false,
                wheelPropagation: false
            }
        }
    },

    async created() {

        console.log('this.desc')
        console.log(this.desc)
        if((this.desc != 'Sair da sessão') && (this.desc != 'Sem resposta' && (this.desc != 'Gamificação')) && (this.desc != 'Estatísticas')){
            await this.$http.get('http://localhost:5000/api/v0/evaluation/getButtonInfo?buttonCode=' + this.buttonCode)
            .then(result => {
                this.modal_text = result.data
            })
            .catch(error => { throw(error) })
        }else if(this.desc != 'Estatísticas'){
            var user = await this.$store.getters.get_session_user
        
            this.$http.get('http://localhost:5000/api/v0/evaluation/getStatistics?userName=' + user.username)
            .then(response => {
                this.statistics_object = JSON.parse(response.data)
            })
            .catch(error => {
                throw(error)
            })
        }
    },

    methods: {
        answer: function() {
            this.$emit("answerQuestion")
        },
        next: function() {
            this.$emit("nextQuestion")
        },
        quit: function() {
            this.$emit("quit")
        },
        cancel: function() {
            this.$emit("cancel")
        }
    }
  }
</script>

<style >
.scroll-area {
  position: relative;
  margin: auto;
  width: 470px;
  height: 110px;
}
</style>