<template>
  <v-form ref="configForm" :disabled="loading">
    <!-- Selecao de Dominio -->
    <section>
      <h4 class="text-h4 mb-4">Selecao de Dominio</h4>

      <!-- Dominio -->
      <v-select
        v-model="selectedDomain"
        :items="domainIds"
        label="Escolha o dominio"
        @change="domainChanged"
        :disabled="domainValues.length == 0"
        :rules="configrules.domain"
        clearable
      />
      <!-- SubDominios -->
      <v-select
        :items="subdomainValues"
        :value="testConfigs.subdomains"
        @input="emitChange('subdomains', $event)"
        label="Escolha os subdominios"
        :disabled="!selectedDomain"
        :rules="configrules.subdomains"
        multiple
        chips
        deletable-chips
      />
    </section>
    <!-- Config  -->
    <v-expand-transition>
      <section v-show="domainsSelectionValid" class="my-6">
        <h4 class="text-h4 mb-4">Configuracao do Teste</h4>
        <!-- Identificador  -->
        <v-text-field
          :value="testConfigs.id"
          @input="emitChange('id', $event.substring(0, 20))"
          :rules="configrules.id"
          label="Identificador"
          counter="20"
          required
          :disabled="!!this.$route.query.editing"
        />

        <!-- Descrição  -->
        <v-text-field
          :value="testConfigs.description"
          @input="emitChange('description', $event.substring(0, 20))"
          :rules="configrules.description"
          counter="100"
          label="Descricao"
          required
        />
        <v-row>
          <!-- Data Inicio -->
          <v-col>
            <v-menu
              :close-on-content-click="true"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="testConfigs.date.start"
                  @input="emitChange('date.start', $event)"
                  label="Data Inicio"
                  append-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  :rules="configrules.date.start"
                  required
                />
              </template>
              <v-date-picker v-model="testConfigs.date.start" />
            </v-menu>
          </v-col>

          <!-- Data Fim -->
          <v-col>
            <v-menu
              :close-on-content-click="true"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  :value="testConfigs.date.finish"
                  @input="emitChange('date.finish', $event)"
                  label="Data Fim"
                  append-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  :rules="configrules.date.finish"
                  required
                />
              </template>
              <v-date-picker v-model="testConfigs.date.finish" />
            </v-menu>
          </v-col>
        </v-row>

        <!-- Nr de Questoes  -->
        <v-text-field
          :value="testConfigs.number_questions"
          @input="emitChange('number_questions', parseInt($event))"
          :rules="configrules.number_questions"
          label="Nr de Questoes"
          required
          type="number"
        />

        <!-- Nível de Dificuldade  -->
        <v-subheader class="px-0">
          Nivel de Dificuldade
          <v-spacer />
          <v-icon
            color="grey lighten-1"
            class="px-0"
            size="25px"
            v-text="'mdi-head-cog'"
          />
        </v-subheader>
        <v-slider
          :value="testConfigs.avg_difficulty"
          @input="emitChange('avg_difficulty', parseInt($event))"
          ticks="always"
          :tick-labels="[1, 2, 3, 4, 5]"
          step="1"
          min="1"
          max="5"
        />

        <v-subheader class="px-0"> Maximo de opcoes por questao </v-subheader>
        <v-slider
          :value="testConfigs.maximum_displayed_answers"
          @input="emitChange('maximum_displayed_answers', parseInt($event))"
          ticks="always"
          :tick-labels="[2, 3, 4, 5, 6]"
          step="1"
          min="2"
          max="6"
        />

        <!-- Tempo de Realizacao  -->
        <v-select
          :value="testConfigs.total_time"
          @input="emitChange('total_time', parseInt($event))"
          :items="[10, 30, 60, 120]"
          label="Tempo de realizacao (min)"
          required
          :rules="configrules.total_time"
          clearable
        />

        <!-- Tipo do teste  -->
        <!-- Value/Input not working, v-model seems to update parent 🤷‍♂️  -->
        <v-radio-group
          v-model="testConfigs.test_type"
          :rules="configrules.test_type"
          label="Tipo de teste"
          row
        >
          <v-radio label="Avalicao" value="assessment" />
          <v-radio label="Afericao" value="gauging" />
        </v-radio-group>

        <!-- Visibilidade  -->
        <v-radio-group
          v-model="testConfigs.visibility"
          :rules="configrules.visibility"
          label="Visibilidade"
          row
        >
          <v-radio label="Publico" value="public" />
          <v-radio label="Privado" value="private" />
        </v-radio-group>

        <!-- Observacoes  -->
        <v-textarea outlined label="Observacoes" v-model="testConfigs.obs" />
      </section>
    </v-expand-transition>
  </v-form>
</template>

<script>
import * as configApi from "@/tests_modulo/utils/api/config";

export default {
  name: "ConfigForm",
  model: {
    prop: "testConfigs",
    event: "change",
  },
  props: { testConfigs: Object },

  data: () => ({
    loading: true,
    selectedDomain: null,
    domainValues: [],

    configrules: {
      domain: [(v) => !!v || "Dominio e obrigatorio"],
      subdomains: [
        (v) =>
          v?.length >= 1 || "Pelo menos um subdominio tem de ser selecionado",
      ],
      id: [
        (v) => !!v || "Identificador e obrigatorio",
        (v) =>
          v?.length <= 20 ||
          "Identificador nao pode ter mais de 20 caracteres ",
      ],
      description: [
        (v) => !!v || "Descricao e obrigatoria",
        (v) =>
          v?.length <= 100 || "Descricao nao pode ter mais de 100 caracteres ",
      ],
      date: {
        start: [(v) => !!v || "Data de inicio e obrigatoria"],
        finish: [(v) => !!v || "Data de fim e obrigatoria"],
      },
      number_questions: [
        (v) => !!v || "Nr de questoes e obrigatorio",
        (v) => Math.round(v) == v || "Nr de questoes tem de ser inteiro",
      ],
      total_time: [(v) => !!v || "Tempo de realizacao e obrigatorio"],
      test_type: [(v) => !!v || "Modo de Visualizacao e obrigatorio"],
      visibility: [(v) => !!v || "Visibilidade e obrigatoria"],
    },
  }),
  methods: {
    fetchDomains() {
      this.loading = true;
      configApi
        .getAvailableDomains()
        .then((data) => {
          this.domainValues = data;
          this.loading = false;
        })
        .catch((err) => {
          this.$emit("fetchFail");
          console.log("Error fetching tests", err);
        });
    },
    domainChanged(evt) {
      this.$emit("change", {
        ...this.testConfigs,
        subdomains: [],
        domain: this.domainValues.find((d) => d._id == evt)?.domain || null,
      });
      this.$refs.configForm.resetValidation();
    },

    async validate() {
      return this.$refs.configForm.validate();
    },
    // Notify parent that a change hapenned (It's not noticed due to v-model use on props :^/)
    emitChange(key, value) {
      this.$emit("change", { ...this.testConfigs, [key]: value });
    },
  },
  computed: {
    /** @returns {any}*/
    domainsSelectionValid() {
      return (
        this?.testConfigs?.subdomains?.length > 0 && this?.testConfigs?.domain
      );
    },
    /** @returns {any}*/
    subdomainValues() {
      return (
        this.domainValues?.find((d) => d._id == this.selectedDomain)
          ?.subdomains || []
      );
    },
    /** @returns {any}*/
    domainIds() {
      return this.domainValues.map((d) => d._id) || [];
    },
  },
  async created() {
    this.fetchDomains();
    const configDomain = this.testConfigs.domain;
    //TODO Domains need Human Readable Ids
    if (configDomain)
      this.selectedDomain = `${configDomain.study_cycle}-${configDomain.scholarity}-${configDomain.description}`;
  },
};
</script>
