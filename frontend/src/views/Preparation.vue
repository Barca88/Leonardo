<template>
  <v-container class="pa-10">
    <AppHeader></AppHeader>
    <NavDraw></NavDraw>
    <h3 class="text-h3 grey--text text--lighten-1 mb-3">
      Preparacao de Testes
    </h3>

    <ConfigForm
      :key="resetCounter"
      v-if="step == 1 && loading == false"
      ref="configForm"
      v-model="testConfigs"
      @fetchFail="snackbarFetchFailed"
    />

    <QuestionSelectForm
      :key="resetCounter"
      v-if="step == 2 && loading == false"
      ref="QuestionSelectForm"
      v-model="questionUpdates.replacingQuestions"
      :replacedQuestions="questionUpdates.replacedQuestions"
      :notReplacedQuestions="questionUpdates.notReplacedQuestions"
      :test="test"
    />

    <TestDisplayDialog
      :show="showTestDisplayDialog"
      @changeVisibility="showTestDisplayDialog = $event"
      :test="test"
    >
      <template v-slot:header>
        Pre visualizacao: {{ test.id }} - {{ test.config.description }}
      </template>
      <template v-slot:actions>
        <v-btn large color="success" @click="submitTest()"> Guardar </v-btn>
        <v-btn large text @click="showTestDisplayDialog = false">
          Fechar
        </v-btn>
      </template>
    </TestDisplayDialog>

    <ButtonMenu
      :step="step"
      @submitTestConfig="submitTestConfig()"
      @submitTest="showTestDisplayDialog = true"
      @resetFields="clearAll()"
      @redoConfig="redoConfig()"
      @updateQuestions="replaceSelectedQuestions()"
    />

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
import ButtonMenu from '@/components/Preparation/ButtonMenu'
import ConfigForm from '@/components/Preparation/ConfigForm'
import QuestionSelectForm from '@/components/Preparation/QuestionSelectForm'
import TestDisplayDialog from '@/components/UI/TestDisplayDialog.vue'
import TextSnackBar from '@/components/UI/TextSnackBar'
//import axios from 'axios'
import AppHeader from '@/components/header.vue'
import NavDraw from '@/components/navDraw'
import Footer from '@/components/Footer'

import * as testsApi from '@/utils/api/tests'
import * as generatorApi from '@/utils/api/generator'

export default {
  name: 'Preparation',
  components: {
    ButtonMenu,
    TextSnackBar,
    ConfigForm,
    QuestionSelectForm,
    TestDisplayDialog,
    AppHeader,
    NavDraw,
    Footer
  },
  data() {
    return {
      //1->config, 2->select questions
      step: 1,
      loading: true,
      testConfigs: {},
      test: null,
      questionUpdates: {
        replacingQuestions: [],
        replacedQuestions: [],
        notReplacedQuestions: 999
      },
      resetCounter: 0,
      showTestDisplayDialog: false,
      snackbar: {
        show: false,
        text: '',
        color: ''
      }
    }
  },
  methods: {
    clearAll() {
      if (this.$route.query.editing) this.$router.push('/preparation')
      else this.clearFields()
    },

    clearFields() {
      this.step = 1
      this.testConfigs = {}
      this.test = null
      this.questionUpdates = {
        replacingQuestions: [],
        replacedQuestions: [],
        notReplacedQuestions: 999
      }
      // Change key to get new components
      this.resetCounter++
      this.testConfigs.avg_difficulty = 3
      this.testConfigs.maximum_displayed_answers = 4
      this.testConfigs.date = {}
    },

    setInitialFields() {
      if (this.$route.query.editing) {
        testsApi
          .getOne(this.$route.query.editing)
          .then((data) => {
            this.test = data
            this.testConfigs = { ...data.config }
            this.testConfigs.id = data.id
            this.step = 2
            this.loading = false
          })
          .catch((err) => {
            this.snackbar = {
              show: true,
              color: 'error',
              text: `O servidor não conseguiu obter o teste para edição !! ☹ Erro: ${err} \n`
            }
          })
      } else {
        this.testConfigs.avg_difficulty = 3
        this.testConfigs.maximum_displayed_answers = 4
        this.testConfigs.total_time = 10
        this.testConfigs.date = {}
        this.loading = false
      }
    },
    redoConfig() {
      this.step = 1
      this.questionUpdates = {
        replacingQuestions: [],
        replacedQuestions: [],
        notReplacedQuestions: 999
      }
    },

    async submitTestConfig() {
      const validForm = await this.$refs.configForm.validate()
      if (validForm) {
        // Had trouble with hours being set on dateStart/Finish :^/
        const dateStart = new Date(this.testConfigs.date.start)
        dateStart.setHours(0, 0, 0, 0)
        const dateFinish = new Date(this.testConfigs.date.finish)
        dateFinish.setHours(0, 0, 0, 0)
        const dateNow = new Date(Date.now())
        dateNow.setHours(0, 0, 0, 0)
        console.log('dateNow :>> ', dateNow)
        console.log('dateeStart:>> ', dateStart)

        //Check if dates are valid
        if (dateStart < dateNow) {
          this.snackbar = {
            show: true,
            color: 'error',
            text: `A data de inicio nao pode ser no passado ☹ \n`
          }
        } else if (dateFinish < dateStart) {
          this.snackbar = {
            show: true,
            color: 'error',
            text: `A data de inicio tem de ser antes da data de fim ☹ \n`
          }
          // Submit config if so
        } else {
          const testId = this.testConfigs.id
          const config = {
            ...this.testConfigs,
            inserted_by: 'Real Human Person'
          }
          delete config.id

          generatorApi
            .generateNew(testId, config, !!this.$route.query.editing)
            .then((data) => {
              // In case there was a return to config
              this.questionUpdates.replacedQuestions = this.questionUpdates.replacingQuestions
              this.questionUpdates.replacingQuestions = []
              this.test = data
              this.step = 2
            })
            .catch((err) => {
              this.snackbar = {
                show: true,
                color: 'error',
                text: `O servidor não conseguiu gerar o teste !! ☹ Erro: ${err} \n`
              }
            })
        }
      }
    },

    snackbarFetchFailed() {
      this.snackbar = {
        show: true,
        color: 'error',
        text: `O servidor não conseguiu obter a informação sobre os dominios !! ☹ \n`
      }
    },

    replaceSelectedQuestions() {
      generatorApi
        .replaceQuestions(this.questionUpdates.replacingQuestions, this.test)
        .then((data) => {
          this.questionUpdates.replacedQuestions = this.questionUpdates.replacingQuestions
          this.questionUpdates.notReplacedQuestions =
            this.test.questions.length -
            this.questionUpdates.replacingQuestions.length
          this.questionUpdates.replacingQuestions = []
          this.test = data
        })
        .catch((err) => {
          this.snackbar = {
            show: true,
            color: 'error',
            text: `O servidor não conseguiu substituir as questoes !! ☹ Erro: ${err} \n`
          }
        })
    },

    submitTest() {
      const config = { ...this.testConfigs, inserted_by: 'Real Human Person' }
      delete config.id
      testsApi
        .saveTest({ ...this?.test, config })
        .then(() => {
          this.snackbar = {
            show: true,
            color: 'success',
            text: `O Teste foi salvo !! 😁 \n`
          }
          this.clearAll()
        })
        .catch((err) => {
          this.snackbar = {
            show: true,
            color: 'error',
            text: `Não foi possivel guardar o teste !! ☹ Erro: ${err} \n`
          }
        })
    }
  },

  created() {
    this.setInitialFields()
  },

  watch: {
    '$route.query'() {
      this.clearFields()
      this.setInitialFields()
    }
  }
}
</script>

<style scoped>
.container {
  margin: 20px auto 80px auto;
  max-width: 1100px;
}
</style>
