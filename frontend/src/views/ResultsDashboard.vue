<template>
  <v-container class="pa-10">
    <h3 class="text-h3 grey--text text--lighten-1 mb-5">Resultados</h3>
    <h4 class="text-h4 mb-4">Dominios e Testes</h4>

    <v-row>
      <v-col cols="12" md="6">
        <DomainForm v-model="domain" @fetchFail="snackbarFetchFailed" />
      </v-col>
      <v-col cols="12" md="6">
        <v-select placeholder="Escolha o editor" />
      </v-col>
    </v-row>

    <v-expand-transition v-if="domain != null">
      <div>
        <v-card class="pa-4">
          <v-row>
            <v-col>
              <TestStatusRow
                :data="resultData[domain].tests.total"
                type="total"
              />
            </v-col>
            <v-col>
              <TestStatusRow
                :data="resultData[domain].tests.assessment"
                type="assessment"
              />
            </v-col>
            <v-col>
              <TestStatusRow
                :data="resultData[domain].tests.gauging"
                type="gauging"
              />
            </v-col>
            <v-col class="d-flex flex-column align-center">
              <h6 class="text-h6 ma-3 text-center">Media Geral</h6>
              <span
                class="mx-1 py-1 text-center"
                style="width: 70px; background-color: #fff2cc"
                >{{ (resultData[domain].generalData.average * 20).toFixed(1) }}
              </span>
              <h6 class="text-h6 ma-3 text-center">Taxa de Acerto</h6>
              <span
                class="mx-1 py-1 text-center"
                style="width: 70px; background-color: #fff2cc"
                >{{
                  (
                    (resultData[domain].generalData.rightAnswers /
                      (resultData[domain].generalData.rightAnswers +
                        resultData[domain].generalData.wrongAnswers)) *
                    100
                  ).toFixed(0) + '%'
                }}
              </span>
            </v-col>
            <v-col class="d-flex flex-column align-center">
              <h6 class="text-h6 ma-3 text-center">Melhor Nota</h6>
              <span
                class="mx-1 py-1 text-center"
                style="width: 70px; background-color: #fff2cc"
                >{{
                  (resultData[domain].generalData.bestGrade * 20).toFixed(1)
                }}
              </span>
              <h6 class="text-h6 ma-3 text-center">Pior Nota</h6>
              <span
                class="mx-1 py-1 text-center"
                style="width: 70px; background-color: #fff2cc"
                >{{
                  (resultData[domain].generalData.worstGrade * 20).toFixed(1)
                }}
              </span>
            </v-col>
          </v-row>
        </v-card>
        <v-card class="mt-5 pa-4">
          <h6 class="text-h6 ma-3 text-center">Próximos Testes</h6>
          <v-data-table
            ref="table"
            :loading="loading"
            :items="tableTests"
            :sort-by="['date']"
            :headers="headers"
            :items-per-page="15"
            :search="search"
            multi-sort
          />
        </v-card>
      </div>
    </v-expand-transition>

    <TextSnackBar
      :color="snackbar.color"
      :text="snackbar.text"
      :show="snackbar.show"
      @close="snackbar.show = false"
    />
  </v-container>
</template>

<script>
import DomainForm from '@/components/Evaluation/DomainForm'
import TextSnackBar from '@/components/UI/TextSnackBar'

import TestStatusRow from '@/components/Dashboards/TestStatusRow.vue'

import * as testsApi from '@/utils/api/tests'
import * as statsApi from '@/utils/api/stats'

export default {
  name: 'Dashboard',
  components: {
    TextSnackBar,
    DomainForm,
    TestStatusRow
  },
  data() {
    return {
      domain: null,
      loading: true,
      resultData: {},
      nearFutureTests: [],
      search: '',
      headers: [
        {
          text: 'Data',
          value: 'date'
        },
        {
          text: 'Identificador',
          value: 'id'
        },
        {
          text: 'Dominio',
          value: 'domain'
        },
        {
          text: 'Tipo',
          value: 'test_type'
        },
        {
          text: 'Dificuldade',
          value: 'avg_difficulty'
        },
        {
          text: 'Duração',
          value: 'total_time'
        },
        {
          text: 'Descrição',
          value: 'description'
        },
        {
          text: 'Autor',
          value: 'inserted_by'
        }
      ],
      snackbar: {
        show: false,
        text: '',
        color: ''
      }
    }
  },
  methods: {
    snackbarFetchFailed() {
      this.snackbar = {
        show: true,
        color: 'error',
        text: `O servidor não conseguiu obter a informação sobre os dominios !! ☹ \n`
      }
    }
  },
  computed: {
    /** @return {any} */
    tableTests() {
      return this.nearFutureTests.map((t) => ({
        ...t.config,
        subdomains: t.config.subdomains.join(', '),
        domain: t.config.domain.description,
        id: t.id,
        date: t.config.date.start
      }))
    }
  },

  created() {
    testsApi
      .getNearFuture()
      .then((data) => {
        this.nearFutureTests = data
        this.loading = false
      })
      .catch(() => {
        this.snackbar = {
          show: true,
          color: 'error',
          text: `Não foi possivel obter a lista de testes ou dominios !! 😫 \n`
        }
      })

    statsApi
      .getResultStats()
      .then((data) => {
        this.resultData = data
        this.loading = false
      })
      .catch(() => {
        this.snackbar = {
          show: true,
          color: 'error',
          text: `Não foi possivel obter a lista de testes ou dominios !! 😫 \n`
        }
      })
  }
}
</script>

<style scoped>
.container {
  margin: 20px auto 80px auto;
  max-width: 1300px;
}
/* css para tornar a aparência mais similar ao template */
.v-data-table /deep/ th {
  background-color: #4b779e;
}
.v-data-table /deep/ tr {
  color: #73879c;
  font-size: 13px;
}
.v-data-table /deep/ tr:nth-child(even) {
  background-color: rgb(245, 245, 245);
}

.v-data-table {
  margin: 20px auto;
  max-width: 1100px;
  margin-bottom: 80px;
}

label {
  color: white;
  padding: 8px;
  font-family: Arial, sans-serif;
  font-weight: bold;
  font-size: 15px;
}
</style>
