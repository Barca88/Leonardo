<template>
  <v-container class="pa-10">
    <h3 class="text-h3 grey--text text--lighten-1 mb-5">
      Realizacao de testes
    </h3>

    <h4 class="text-h4 mb-4">Escolha o Dominio</h4>

    <DomainForm v-model="domain" @fetchFail="snackbarFetchFailed" />

    <v-expand-transition>
      <v-data-table
        v-show="domain != null"
        ref="table"
        :loading="loading"
        :items="tableTests"
        :sort-by="['id']"
        :headers="headers"
        :items-per-page="15"
        :search="search"
        multi-sort
      >
        <template v-slot:top>
          <!-- Heading for mobile -->
          <h5 class="text-h5 px-4 hidden-md-and-up">Gestao de Testes</h5>
          <v-divider class="mx-2 hidden-md-and-up" />

          <v-toolbar flat color="white">
            <!-- Heading for larger screens -->
            <v-toolbar-title class="hidden-sm-and-down">
              Escolha de Teste
            </v-toolbar-title>
            <v-divider class="mx-4 hidden-sm-and-down" inset vertical />
            <v-spacer class="hidden-sm-and-down" />

            <!-- Search Bar -->
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Pesquisa"
              single-line
              hide-details
              class="mr-5"
            />
          </v-toolbar>
        </template>

        <template v-slot:[`item.options`]="{ item }">
          <div class="d-flex">
            <v-btn
              small
              text
              link
              :to="`/tests/evaluation/${item.id}`"
              class="mx-1"
            >
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn text small class="warning--text change-font" v-on="on">
                    <v-icon v-text="'mdi-pen'" />
                  </v-btn>
                </template>
                <span>Realizar</span>
              </v-tooltip>
            </v-btn>
          </div>
        </template>
      </v-data-table>
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
import DomainForm from "@/tests_modulo/components/Evaluation/DomainForm";
import TextSnackBar from "@/tests_modulo/components/UI/TextSnackBar";

import * as testsApi from "@/tests_modulo/utils/api/tests";

export default {
  name: "Evaluation",
  components: {
    TextSnackBar,
    DomainForm,
  },
  data() {
    return {
      domain: null,
      loading: true,
      search: "",
      tests: [],
      headers: [
        {
          text: "Identificador",
          value: "id",
        },
        {
          text: "Descrição",
          value: "description",
        },
        {
          text: "Dominio",
          value: "domain",
        },
        {
          text: "SubDominios",
          value: "subdomains",
        },
        {
          text: "Autor",
          value: "inserted_by",
        },
        {
          text: "Ultima Atualizacao",
          value: "last_updated",
        },
        {
          text: "Opções",
          value: "options",
          sortable: false,
        },
      ],
      snackbar: {
        show: false,
        text: "",
        color: "",
      },
    };
  },
  methods: {
    snackbarFetchFailed() {
      this.snackbar = {
        show: true,
        color: "error",
        text: `O servidor não conseguiu obter a informação sobre os dominios !! ☹ \n`,
      };
    },
  },

  computed: {
    /** @return {any} */
    tableTests() {
      if (this.domain) {
        const [study_cycle, scholarity, description] = this.domain.split("-");
        return this.tests
          .filter(
            (t) =>
              t.config.domain.study_cycle === study_cycle &&
              t.config.domain.scholarity === scholarity &&
              t.config.domain.description === description
          )
          .map((t) => ({
            ...t.config,
            subdomains: t.config.subdomains.join(", "),
            domain: t.config.domain.description,
            id: t.id,
          }));
      } else return [];
    },
  },

  created() {
    this.loading = true;

    testsApi
      .getAll()
      .then((data) => {
        this.tests = data;
        this.loading = false;
      })
      .catch(() => {
        this.snackbar = {
          show: true,
          color: "error",
          text: `Não foi possivel obter a lista de testes ou dominios !! 😫 \n`,
        };
      });
  },
};
</script>

<style scoped>
.container {
  margin: 20px auto 80px auto;
  max-width: 1100px;
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
