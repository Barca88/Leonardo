<template>
  <v-container class="pa-10">
    <AppHeader></AppHeader>
    <NavDraw></NavDraw>
    
      <v-col cols="12" md="3">
        <v-card>
          <v-list>
            <v-list-item class="d-flex align-center">
              Numero de Aluno : {{ this.$store.state.user.studentNumber }}
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    

    <v-card
      v-if="step == 4 && result"
      class="mx-auto"
      style="width: fit-content"
    >
      <TestResultOverview
        :test="result"
        style="max-width: 1100px"
        class="d-flex flex-column align-center mx-auto"
      >
      </TestResultOverview>
      <v-col class="d-flex justify-center align-center">
        <v-btn
          class="ma-2 px-10"
          large
          color="success"
          style="max-width: 300px"
          @click="returnStep3()"
        >
          Ver Resultado
        </v-btn>
        <v-btn
          class="ma-2 px-10"
          large
          color="error"
          style="max-width: 300px"
          link
          to="/evaluation"
        >
          Sair
        </v-btn>
      </v-col>
    </v-card>

    <v-card v-if="step == 3" class="d-flex flex-column">
      <h4 class="pt-6 pb-0 text-h4 text-center" color="primary ">
        Resultado :
      </h4>

      <v-card-text
        class="d-flex flex-column"
        style="overflow-y: auto; overflow-x: hidden"
      >
        <v-container>
          <v-row justify="center">
            <v-col cols="12" md="10" lg="6" class="d-flex justify-space-around">
              <v-card class="pa-3" width="fit-content">
                <v-card-title> Questoes </v-card-title>
                <v-list>
                  <v-list-item class="d-flex align-center">
                    Apresentadas : {{ result["questions"].length }}
                  </v-list-item>

                  <v-list-item class="d-flex align-center">
                    Certas :
                    {{ result["questions"].filter((q) => q["result"] == 1).length }}
                  </v-list-item>
                  <v-list-item class="d-flex align-center">
                    Erradas :
                    {{ result["questions"].filter((q) => q["result"] == 0).length }}
                  </v-list-item>
                  <v-list-item class="d-flex align-center">
                    Taxa de acerto : {{result["result"]}} %
                  </v-list-item>
                  <v-list-item class="d-flex align-center">
                    Resultado : {{ (result.result  / 10) * 2 }}
                  </v-list-item>
                </v-list>
              </v-card>
            </v-col>
            <v-col class="d-flex flex-column justify-center align-center">
              <v-btn
                class="ma-2 px-10"
                large
                color="success"
                style="max-width: 300px"
                @click="startStep4()"
              >
                Ver Resolucao
              </v-btn>
              <v-btn
                class="ma-2 px-10"
                large
                color="error"
                style="max-width: 300px"
                link
                to="/testresults"
              >
                Sair
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    <TextSnackBar
      :color="snackbar.color"
      :text="snackbar.text"
      :show="snackbar.show"
      @close="snackbar.show = false"
    />
    <Footer class="mt-5"></Footer>
  </v-container>
</template>

<script>
import TextSnackBar from '@/components/UI/TextSnackBar'
import TestResultOverview from '@/components/Evaluation/TestResultOverview'
import AppHeader from '@/components/header.vue'
import NavDraw from '@/components/navDraw'
import Footer from '@/components/Footer'

import * as evaluationApi from '@/utils/api/evaluation'

export default {
    name: 'Evaluation',
    components: {
        TextSnackBar,
        TestResultOverview,
        AppHeader,
        NavDraw,
        Footer
    },
    data() {
        return {
            //1->overview, 2->answering, 3-> result, 3->result details
            step: 1,
            loading: true,
            test: null,
            currentQuestion: 0,
            timeCurrentQuestion: 999,
            timeLeft: 999,
            answers: [],
            result: null,
            check: '',
            exists: 0,
            snackbar: {
                show: false,
                text: '',
                color: ''
            }
        }
    },
    methods: {
        startStep4() {
            this.step = 4
        },
        returnStep3() {
            this.step = 3
        }
    },
    async created() {
      
        await evaluationApi
            .getOneEval(this.$route.params['testid'])
            .then((response) => {
              console.log(response)
                this.result = response.tests[0]
                this.step = 3
                console.log('ending 1')
                console.log(this.result)
            })
            .catch(() => {
                this.snackbar = {
                    show: true,
                    color: 'error',
                    text: `Não foi possivel obter o teste !! 😫 \n`
                }
            })


        




    }
}
</script>
<style>
.v-carousel{
  height: fit-content !important;
}
</style>

