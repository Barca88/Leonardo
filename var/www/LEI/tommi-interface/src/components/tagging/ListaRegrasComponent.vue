<template>
  <div id="folios">
    <v-row class="text-center">
      <v-col>
        <h2>Sistema de Anotação Automática de Textos</h2>
      </v-col>
    </v-row>
    <hr />
    <br />
    <v-data-table
      :headers="headers"
      :items="regras"
      :items-per-page="15"
      :search="search"
      class="mytable"
      multi-sort
      >
      <template v-slot:top>
        <v-row>
          <v-toolbar flat color="white">
            <v-col cols="3">
              <v-toolbar-title>{{ $t("tagging.regras") }}</v-toolbar-title>
            </v-col>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-col cols="7">
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                :label="`${$t('navd.se')}`"
                single-line
                hide-details
                class="mr-5"
              ></v-text-field>
            </v-col>
            <v-col cols="2">
              <v-tooltip top>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    class="ma-2"
                    color="#4b779e"
                    @click="dialog_nova_regra = true"
                    dark
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </template>
                <span>Nova Regra</span>
              </v-tooltip>
            </v-col>
          </v-toolbar>
        </v-row>
      </template>
      <template v-slot:header.old="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.new="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.options="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:item.options="{ item }">
        <v-icon small class="mr-2" @click="openRemoveDialog(item)">
          mdi-trash-can
        </v-icon>
      </template>
    </v-data-table>

    <!-- NOVA REGRA -->
    <v-dialog v-model="dialog_nova_regra" width="500">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>Nova Regra</v-card-title>

        <v-card-text>
          <v-row>
            <v-col cols="6">
              <v-text-field v-model="nova_regra_antiga" label="Antiga" outlined></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="nova_regra_atualizada" label="Atualizada" outlined></v-text-field>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog_nova_regra = false">Fechar</v-btn>
          <v-btn color="primary" text @click="adicionaRegra()">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- REMOVER REGRA -->
    <v-dialog v-model="dialog_remove_regra" width="500">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>Remover Regra</v-card-title>
        <v-card-text>
            <h3> Tem a certeza que pretende remover a regra ?</h3>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog_remove_regra = false">Fechar</v-btn>
          <v-btn color="primary" text @click="removeRegra()">Remover</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>



<script>
import axios from "axios";
const lhost = 'https://tommi2.di.uminho.pt/api'
//const lhost = "http://localhost:5000";

export default {
  components: {
  },
  data() {
    return {
      // Lista de Tags
      headers: [
        {
          text: `${this.$t("tagging.old")}`,
          align: "start",
          value: "old",
        },
        {
          text: `${this.$t("tagging.new")}`,
          value: "new",
        },
        {
          text: `${this.$t("def.opt")}`,
          value: "options",
          sortable: false,
        },
      ],
      search: "",
      regras: [],

      // EDIT AND NOVA TAG
      dialog_regras_atualizacao: false,
      dialog_nova_regra: false,
      dialog_remove_regra: false,
      nova_regra_antiga: "",
      nova_regra_atualizada: "",
      remove_regra_antiga: "",
      remove_regra_atualizada: ""
    };
  },
  methods: {
    onUpdate() {
      axios
        .get(lhost + "/tagging/regras")
        .then((response) => {
          this.regras = response.data.regras;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    adicionaRegra: function() {
      var novaRegra = {};
      novaRegra["old"] = this.nova_regra_antiga;
      novaRegra["new"] = this.nova_regra_atualizada;
      this.nova_regra_antiga = "";
      this.nova_regra_atualizada = "";
      this.dialog_nova_regra = false;
      axios
        .post(lhost + "/tagging/regras/adiciona", {regra: novaRegra})
        .then(() => {
          this.onUpdate()
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    openRemoveDialog: function(item) {
      this.remove_regra_antiga = item.old;
      this.remove_regra_atualizada = item.new;
      this.dialog_remove_regra = true;
    },
    removeRegra: function () {
      this.dialog_remove_regra = false;
      var regraRemover = {}
      regraRemover["old"] = this.remove_regra_antiga;
      regraRemover["new"] = this.remove_regra_atualizada;
      this.remove_regra_antiga = "";
      this.remove_regra_atualizada = "";
      axios
        .post(lhost + "/tagging/regras/remove", {regra: regraRemover})
        .then(() => {
          this.onUpdate()
        })
        .catch((e) => {
          this.errors.push(e);
        });
    }
  },
  created() {
    this.onUpdate();
  },
};
</script>
<style scoped>
@media print {
  body {
    overflow: auto;
    height: auto;
  }
  .page-break {
    display: block;
    page-break-before: always;
  }
}
/* .tommitable .v-data-table .table{ */
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
#folios * {
  box-sizing: border-box;
}
#folios {
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
b {
  font-size: 20px;
}
</style>
