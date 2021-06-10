<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <h4 class="py-6 text-h4 text-center" color="primary ">Configuracao</h4>
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

                <v-list-item class="d-flex align-center">
                  Dominio :
                  <v-list>
                    <v-list-item class="d-flex align-center">
                      Descricao : {{ test.config.domain.description }}
                    </v-list-item>
                    <v-list-item class="d-flex align-center">
                      Escolaridade : {{ test.config.domain.scholarity }}
                    </v-list-item>
                    <v-list-item class="d-flex align-center">
                      Ciclo de estudo : {{ test.config.domain.study_cycle }}
                    </v-list-item>
                  </v-list>
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Subdominios : {{ test.config.subdomains.join(', ') }}
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Data :
                  <v-list>
                    <v-list-item class="d-flex align-center">
                      Inicio : {{ test.config.date.start }}
                    </v-list-item>
                    <v-list-item class="d-flex align-center">
                      Fim : {{ test.config.date.finish }}
                    </v-list-item>
                  </v-list>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <v-list>
                <v-list-item class="d-flex align-center">
                  Numero de Questoes : {{ test.config.number_questions }}
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Dificuldade :
                  <v-rating
                    class="ps-2"
                    :value="parseInt(test.config.avg_difficulty)"
                  >
                    <template v-slot:item="props">
                      <v-icon
                        :color="props.isFilled ? 'orange' : 'grey lighten-1'"
                        class="px-0"
                        size="25px"
                        v-text="'mdi-head-cog'"
                      />
                    </template>
                  </v-rating>
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Maximo de Opcoes por Questoes :
                  {{ test.config.maximum_displayed_answers }}
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Tempo de realizacao :
                  {{ test.config.total_time }}
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Tipo de teste :
                  {{ test.config.test_type }}
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Visibilidade :
                  {{ test.config.visibility }}
                </v-list-item>

                <v-list-item class="d-flex align-center">
                  Obervacoes :
                  {{ test.config.obs }}
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-col cols="12" md="4" class="d-flex flex-column">
        <h4 class="py-6 text-h4 text-center" color="primary ">Ajustes</h4>
        <v-card style="flex-grow: 1">
          <v-list>
            <v-list-item class="d-flex align-center">
              Dificuldade :
              {{
                `${test.compromises.avg_difficulty >= 0 ? '+ ' : ' '}
            ${test.compromises.avg_difficulty}`
              }}
            </v-list-item>
            <v-list-item class="d-flex align-center">
              Numero de questoes :
              {{
                `${test.compromises.number_questions >= 0 ? '+ ' : '- '}
            ${test.compromises.number_questions}`
              }}
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    test: Object
  }
}
</script>
