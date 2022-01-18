<template>
  <div>
    <v-data-table
      ref="table"
      :loading="loading"
      :items="tableTests"
      :sort-by="['id']"
      :headers="headers"
      :items-per-page="15"
      :search="search"
      @current-items="setItems($event)"
      multi-sort
    >
      <template v-slot:top>
        <!-- Heading for mobile -->
        <h5 class="text-h5 px-4 hidden-md-and-up">Gestao de Testes</h5>
        <v-divider class="mx-2 hidden-md-and-up" />

        <v-toolbar flat color="white">
          <!-- Heading for larger screens -->
          <v-toolbar-title class="hidden-sm-and-down">
            Gestao de Testes
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

          <!-- New Test Button -->
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-on="on"
                v-bind="attrs"
                class="blue-grey darken-4 white--text mx-2"
                link
                to="/tests/preparation"
              >
                <v-icon small v-text="'mdi-file-plus-outline'" />
              </v-btn>
            </template>
            <span>Gerar Novo Teste</span>
          </v-tooltip>

          <!-- Print Tests Button -->
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-on="on"
                v-bind="attrs"
                class="blue-grey darken-4 white--text mx-2"
                @click="print()"
              >
                <v-icon small v-text="'mdi-printer'" />
              </v-btn>
            </template>
            <span>Imprimir Testes</span>
          </v-tooltip>
        </v-toolbar>
      </template>

      <template v-slot:[`item.options`]="{ item }">
        <div class="d-flex">
          <!-- View Test Button -->
          <v-btn
            small
            icon
            class="info--text mx-1"
            @click="
              selectedTest = tests.find((x) => x.id === item.id);
              showTestDisplayDialog = true;
            "
          >
            <v-icon small v-text="'mdi-eye'" />
          </v-btn>

          <!-- Edit Test Button -->
          <!-- TODO Confirm that wants to edit -->
          <v-btn
            small
            icon
            class="warning--text mx-1"
            link
            :to="`/tests/preparation?editing=${item.id}`"
          >
            <v-icon small v-text="'mdi-lead-pencil'" />
          </v-btn>

          <!-- Delete Test Button -->
          <v-btn
            small
            icon
            class="error--text mx-1"
            @click="
              selectedTest = tests.find((x) => x.id === item.id);
              showTestDeleteDialog = true;
            "
          >
            <v-icon small v-text="'mdi-delete'" />
          </v-btn>
        </div>
      </template>
    </v-data-table>

    <TestDisplayDialog
      :show="showTestDisplayDialog"
      @changeVisibility="showTestDisplayDialog = $event"
      :test="selectedTest"
    />

    <DeleteTestDialog
      :show="showTestDeleteDialog"
      @changeVisibility="showTestDeleteDialog = $event"
      @delete="deleteTest($event)"
      :test="selectedTest"
    />

    <TextSnackBar
      :color="snackbar.color"
      :text="snackbar.text"
      :show="snackbar.show"
      @close="snackbar.show = false"
    />
  </div>
</template>

<script>
import * as testsApi from "@/tests_modulo/utils/api/tests";
import TestDisplayDialog from "@/tests_modulo/components/UI/TestDisplayDialog.vue";
import DeleteTestDialog from "@/tests_modulo/components/Management/DeleteTestDialog.vue";
import TextSnackBar from "@/tests_modulo/components/UI/TextSnackBar";

export default {
  name: "Management",
  components: { TestDisplayDialog, DeleteTestDialog, TextSnackBar },
  data() {
    return {
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
      search: "",
      loading: true,
      tests: [],
      showTestDisplayDialog: false,
      showTestDeleteDialog: false,
      selectedTest: {},
      printableItems: [],
      snackbar: {
        show: false,
        text: "",
        color: "",
      },
    };
  },
  computed: {
    /** @returns {any} */
    tableTests() {
      return this.tests.map((t) => ({
        ...t.config,
        subdomains: t.config.subdomains.join(", "),
        domain: t.config.domain.description,
        id: t.id,
      }));
    },
  },
  methods: {
    fetchTests() {
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
            text: `Não foi possivel obter a lista de testes !! 😫 \n`,
          };
        });
    },

    deleteTest(id) {
      this.loading = true;

      const test = this.tests.find((t) => t.id == id);

      testsApi
        .deleteOne(id)
        .then(() => {
          this.tests = this.tests.filter((t) => t.id != id);
          this.snackbar = {
            show: true,
            color: "warning",
            text: `O teste ${test.id} - ${test.description} foi removido com sucesso !! 😉 \n`,
          };
          this.loading = false;
          this.showTestDeleteDialog = false;
        })
        .catch(() => {
          this.snackbar = {
            show: true,
            color: "error",
            text: `Ocorreu um erro ao remover o teste ${test.id} - ${test.description} !! 😫 \n`,
          };
        });
    },

    remove(itemId) {
      alert(`💀 removed ${itemId}`);
    },
    confirmQuestions() {
      alert(`✔ Checking questions...`);
    },
    print() {
      alert(
        `🖨 Printing... ${JSON.stringify(
          this.printableItems.map((i) => i.id),
          null,
          2
        )}`
      );
    },
    setItems(visibleItems) {
      this.printableItems = visibleItems;
    },
  },
  created() {
    this.fetchTests();
  },
};
</script>

<style scoped>
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
