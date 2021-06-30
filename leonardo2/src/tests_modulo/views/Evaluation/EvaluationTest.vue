<template>
  <v-main class="pa-10">
    <v-row justify="space-around" class="mb-0">
      <v-col cols="12" md="3">
        <h3 class="text-h3 grey--text text--lighten-1">Realizacao de teste:</h3>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-row class="ma-0">
            <v-col cols="12" md="6">
              <v-list>
                <v-list-item class="d-flex align-center">
                  Identificador : {{ test.id }}
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Descricao : {{ test.config.description }}
                </v-list-item>
              </v-list>
            </v-col>
            <v-col cols="12" md="6">
              <v-list>
                <v-list-item class="d-flex align-center">
                  Dominio :
                  <v-list>
                    <v-list-item
                      style="min-height: 25px"
                      class="d-flex align-center"
                    >
                      Descricao : {{ test.config.domain.description }}
                    </v-list-item>
                    <v-list-item
                      style="min-height: 25px"
                      class="d-flex align-center"
                    >
                      Escolaridade : {{ test.config.domain.scholarity }}
                    </v-list-item>
                    <v-list-item
                      style="min-height: 25px"
                      class="d-flex align-center"
                    >
                      Ciclo de estudo : {{ test.config.domain.study_cycle }}
                    </v-list-item>
                  </v-list>
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Subdominios : {{ test.config.subdomains.join(', ') }}
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card>
          <v-list>
            <v-list-item class="d-flex align-center">
              Nome : {{ 'Jonas Soares de Sousa' }}
            </v-list-item>
            <v-list-item class="d-flex align-center">
              Numero de Aluno : {{ 'a11111' }}
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>

    <section
      v-if="step == 1 && loading == false"
      class="d-flex flex-column align-center"
    >
      <TestDetails :test="test" />
      <v-btn color="warning" large @click="startStep2()">Iniciar</v-btn>
    </section>

    <section
      v-if="step == 2"
      style="max-width: 1100px"
      class="d-flex flex-column align-center mx-auto"
    >
      <v-carousel
        hide-delimiters
        :show-arrows="false"
        class="ma-4"
        height="fit-content"
        v-model="currentQuestion"
      >
        <v-carousel-item v-for="(q, i) in test.questions" :key="i">
          <v-card
            light
            class="ma-2 pa-2 d-flex flex-column"
            style="min-height: 95%"
          >
            <v-card-title>
              <h4>
                {{ i + 1 + '. ' + q.id }}
              </h4>
              <v-spacer />
              <div class="d-flex flex-column">
                <div class="d-flex align-center">
                  <v-progress-linear
                    :color="
                      timeLeft < 10
                        ? 'error'
                        : timeLeft < 20
                        ? 'warning'
                        : 'info'
                    "
                    height="10"
                    style="width: 200px"
                    :value="
                      Math.floor(
                        ((timeCurrentQuestion - timeLeft) /
                          timeCurrentQuestion) *
                          100
                      )
                    "
                    striped
                  />
                  <v-icon class="px-1" v-text="'mdi-timer-outline'" />
                </div>
              </div>
            </v-card-title>
            <v-card-subtitle
              class="d-flex align-center justify-space-between align-center"
            >
            </v-card-subtitle>
            <v-card-text>
              {{ q.header }}
            </v-card-text>
            <!-- Solucoes -->
            <v-card-text class="pt-0">
              <v-form>
                <v-radio-group
                  :value="answers[i]"
                  @change="updateAnswers(i, $event)"
                >
                  <v-radio
                    v-for="(answer, n) in q.body"
                    :key="n"
                    class="my-2"
                    :label="answer.answer"
                    :value="answer.answer"
                  />
                </v-radio-group>
              </v-form>
            </v-card-text>
            <v-spacer />
            <v-card-actions
              class="
                d-flex
                justify-center justify-md-start
                flex-wrap
                align-center
                mx-4
              "
            >
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    v-on="on"
                    v-bind="attrs"
                    color="error"
                    class="white--text ma-2"
                    @click="startStep3()"
                  >
                    <v-icon v-text="'mdi-door-open'" />
                  </v-btn>
                </template>
                <span>Abortar</span>
              </v-tooltip>

              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    v-on="on"
                    v-bind="attrs"
                    color="info"
                    class="white--text ma-2"
                    @click="'ajuda'"
                  >
                    <v-icon v-text="'mdi-lightbulb'" />
                  </v-btn>
                </template>
                <span>Ajuda</span>
              </v-tooltip>

              <v-tooltip v-if="i != test.questions.length - 1" top>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    v-on="on"
                    v-bind="attrs"
                    color="warning"
                    class="ma-2"
                    :disabled="answers[i] === null"
                    @click="nextQuestion()"
                  >
                    <v-icon v-text="'mdi-arrow-right-circle-outline'" />
                  </v-btn>
                </template>
                <span>Proxima</span>
              </v-tooltip>

              <v-tooltip v-if="i == test.questions.length - 1" top>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    v-on="on"
                    v-bind="attrs"
                    color="success"
                    class="white--text ma-2"
                    :disabled="answers[i] === null"
                    @click="startStep3()"
                  >
                    <v-icon v-text="'mdi-check-decagram'" />
                  </v-btn>
                </template>
                <span>Submeter</span>
              </v-tooltip>
            </v-card-actions>
          </v-card>
        </v-carousel-item>
      </v-carousel>
    </section>

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
          to="/tests/evaluation"
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
        <v-main>
          <v-row justify="center">
            <v-col cols="12" md="10" lg="6" class="d-flex justify-space-around">
              <v-card class="pa-3" width="fit-content">
                <v-card-title> Questoes </v-card-title>
                <v-list>
                  <v-list-item class="d-flex align-center">
                    Apresentadas : {{ result.questions.length }}
                  </v-list-item>

                  <v-list-item class="d-flex align-center">
                    Certas :
                    {{ result.questions.filter((q) => q.result == 1).length }}
                  </v-list-item>
                  <v-list-item class="d-flex align-center">
                    Erradas :
                    {{ result.questions.filter((q) => q.result == 0).length }}
                  </v-list-item>
                  <v-list-item class="d-flex align-center">
                    Taxa de acerto : {{ (result.result * 100).toFixed(0) }} %
                  </v-list-item>
                  <v-list-item class="d-flex align-center">
                    Resultado : {{ (result.result * 100).toFixed(0) }} / 100
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
                to="/tests/evaluation"
              >
                Sair
              </v-btn>
            </v-col>
          </v-row>
        </v-main>
      </v-card-text>
    </v-card>
    <TextSnackBar
      :color="snackbar.color"
      :text="snackbar.text"
      :show="snackbar.show"
      @close="snackbar.show = false"
    />
  </v-main>
</template>

<script>
import TextSnackBar from '@/tests_modulo/components/UI/TextSnackBar'
import TestDetails from '@/tests_modulo/components/UI/TestDetails'
import TestResultOverview from '@/tests_modulo/components/Evaluation/TestResultOverview'

import * as evaluationApi from '@/tests_modulo/utils/api/evaluation'

export default {
  name: 'Evaluation',
  components: {
    TextSnackBar,
    TestDetails,
    TestResultOverview
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
      snackbar: {
        show: false,
        text: '',
        color: ''
      }
    }
  },
  methods: {
    tick() {
      if (this.step == 2) {
        this.timeLeft--
        if (this.timeLeft == 0) this.nextQuestion()

        setTimeout(() => {
          this.tick()
        }, 1000)
      }
    },
    nextQuestion() {
      if (this.currentQuestion == this.test.questions.length - 1) {
        this.startStep3()
      } else {
        this.currentQuestion++
        this.timeCurrentQuestion =
          this.test.questions[this.currentQuestion].answering_time
        this.timeLeft = this.test.questions[this.currentQuestion].answering_time
      }
    },
    updateAnswers(i, val) {
      const newAnswers = { ...this.answers }
      newAnswers[i] = val
      this.answers = newAnswers
    },
    startStep2() {
      this.step = 2
      this.tick()
    },
    startStep3() {
      this.step = 3
      this.loading = true

      const resolution = { ...this.test }

      resolution.questions.forEach((q, i) => {
        q.body.forEach((a) => {
          if (a.answer.localeCompare(this.answers[i]) == 0) {
            a.selected = true
          } else {
            a.selected = false
          }
        })
      }),
        (resolution.student_id =
          'José Estevão Soares Carvalho de Cunha e Sousa')

      evaluationApi
        .submit(resolution)
        .then((data) => {
          this.loading = false
          this.result = data
        })
        .catch(() => {
          this.snackbar = {
            show: true,
            color: 'error',
            text: `Não foi possivel submeter a resolucao !! 😫 \n`
          }
        })
    },
    startStep4() {
      this.step = 4
    },
    returnStep3() {
      this.step = 3
    }
  },
  created() {
    this.loading = true
    evaluationApi
      .getOne(this.$route.params['testid'])
      .then((data) => {
        this.test = data
        this.test.questions.forEach((_, i) => {
          this.answers[i] = null
        })
        this.timeCurrentQuestion =
          this.test.questions[this.currentQuestion].answering_time
        this.timeLeft = this.test.questions[this.currentQuestion].answering_time
        this.loading = false
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
