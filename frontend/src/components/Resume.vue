<template>    
    <v-card>
        <HeaderModal/>
        <v-container>
            <div>
                <v-row cols="12">
                    <v-col cols="12">
                        <v-row>
                            <v-card class="ml-4 mt-1" color="red" flat height="65px" width="70px">
                                <div>
                                    <v-icon v-bind:style="'border: 0px solid red; color: white; border-radius:0%; size: 30; height: 65px; width: 70px;'">mdi-file-document</v-icon>
                                </div>
                            </v-card>
                            <v-card class="ml-0" flat="">
                                <v-card-title style="font-size: 20px;"><b>Resumo da sessão</b></v-card-title>
                                <v-card-text style="font-size: 16px;">
                                    <p> Nível: {{ this.statsObj.user_level }} </p>
                                    <p> Número total de questões: {{ this.statsObj.total_questions }} </p>
                                    <p> Número de perguntas corretas: {{ this.statsObj.questions_right }} </p>
                                    <p> Número de perguntas incorretas: {{ this.statsObj.questions_wrong }} </p>
                                    <p> Tempo de resposta: {{ this.statsObj.answers_time }} </p>
                                </v-card-text>
                            </v-card>
                        </v-row>
                    </v-col>
                </v-row>
            </div>
        </v-container>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn class="white--text text-capitalize; mr-3" color="#00cc99" @click="quit(), dialog_resume = false" v-bind="attrs" v-on="on"><v-icon>mdi-door-open</v-icon></v-btn>
                </template>
                <span>Sair</span>
            </v-tooltip>
        </v-card-actions>
    </v-card>
</template>

<script>
  import HeaderModal from './Header_modal';

  export default {
    name: 'Resume',

    props: ['statsObj'],

    components: {
        HeaderModal
    },

    methods: {
        quit: function() {
            this.$emit("quit")
        }
    }
  }
</script>
