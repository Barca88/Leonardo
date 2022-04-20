<template>
  <section class="my-6">
    <v-row class="ma-0" align="start" no-gutters>
      <!-- Submit Config  -->
      <v-col v-if="step == 1" style="flex-grow: 0">
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              class="amber accent-3 white--text mr-2 my-1"
              @click="$emit('submitTestConfig')"
            >
              <v-icon v-text="'mdi-check-decagram'" />
            </v-btn>
          </template>
          <span>Submeter Configuracao</span>
        </v-tooltip>
      </v-col>

      <!-- Submit Test  -->
      <v-col v-if="step == 2 || editing" style="flex-grow: 0">
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              class="amber accent-3 white--text mr-2 my-1"
              @click="$emit('submitTest')"
            >
              <v-icon v-text="'mdi-checkbox-marked-outline'" />
            </v-btn>
          </template>
          <span>Salvar Teste</span>
        </v-tooltip>
      </v-col>

      <!-- Go back to config  -->
      <v-col style="flex-grow: 0">
        <v-tooltip v-if="step == 2" top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              class="green accent-3 white--text mr-2 my-1"
              @click="$emit('redoConfig')"
            >
              <v-icon v-text="'mdi-cog-counterclockwise'" />
            </v-btn>
          </template>
          <span>Voltar a configuracao</span>
        </v-tooltip>
      </v-col>

      <!-- Reset Form  -->
      <v-col style="flex-grow: 0">
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              class="green accent-3 white--text mr-2 my-1"
              @click="$emit('resetFields')"
            >
              <v-icon v-text="'mdi-broom'" />
            </v-btn>
          </template>
          <span>Limpar Tudo</span>
        </v-tooltip>
      </v-col>

      <!-- Recycle Questions  -->
      <v-col style="flex-grow: 0">
        <v-tooltip v-if="step == 2" top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              class="green--text lighten-1 mr-2 my-1"
              @click="$emit('updateQuestions')"
            >
              <v-icon v-text="'mdi-recycle'" />
            </v-btn>
          </template>
          <span>Reciclar Questoes</span>
        </v-tooltip>
      </v-col>

      <!-- Exit  -->
      <v-col style="flex-grow: 0">
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              class="green accent-3 white--text mr-2 my-1"
            >
              <v-icon v-text="'mdi-door-open'" />
            </v-btn>
          </template>
          <span>{{ $t('opc.sair') }}</span>
        </v-tooltip>
      </v-col>
    </v-row>
    <v-row class="ma-0" no-gutters>
      <!-- About  -->
      <v-col style="flex-grow: 0">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              class="blue-grey darken-4 white--text mr-2 my-1"
            >
              <v-icon v-text="'mdi-information-outline'" />
            </v-btn>
          </template>
          <span>Acerca</span>
        </v-tooltip>
      </v-col>

      <!-- Help  -->
      <v-col style="flex-grow: 0">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              class="blue-grey darken-4 white--text mr-2 my-1"
            >
              <v-icon v-text="'mdi-lightbulb'" />
            </v-btn>
          </template>
          <span>Ajuda</span>
        </v-tooltip>
      </v-col>
    </v-row>
  </section>
</template>

<script>
export default {
  name: 'ButtonMenu',
  props: { step: Number },
  computed: {
    editing() {
      return this.$route.query.editing
    }
  }
}
</script>