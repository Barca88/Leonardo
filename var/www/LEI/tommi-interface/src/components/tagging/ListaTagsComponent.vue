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
      :items="tags"
      :items-per-page="15"
      :sort-by="['_id']"
      :search="search"
      class="mytable"
      multi-sort
      ><template v-slot:top>
        <v-row>
          <v-toolbar flat color="white">
            <v-col cols="3">
              <v-toolbar-title>{{ $t("tagging.lista") }}</v-toolbar-title>
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
              <NovaTagComponent @listChanged="refresh()" />
            </v-col>
          </v-toolbar>
        </v-row>
      </template>
      <template v-slot:header._id="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.atividade="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:item.atividade="{ item }">
        <template v-if="item.ativa">
          <p>Ativa</p>
        </template>
        <template v-else>
          <p>Inativa</p>
        </template>
      </template>
      <template v-slot:header.cor="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:item.cor="{ item }">
        <v-btn :color="item.cor"></v-btn>
      </template>
      <template v-slot:header.options="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:item.options="{ item }">
        <template v-if="item.tag == 'localidade'">
          <v-icon small class="mr-2" @click="openEditDialog(item)">
            mdi-eye
          </v-icon>
        </template>
        <template v-else>
          <v-icon small class="mr-2" @click="openEditDialog(item)">
            mdi-eye
          </v-icon>
          <v-icon small @click="openRemoveDialog(item)"> mdi-trash-can </v-icon>
        </template>
      </template>
    </v-data-table>

    <!-- EDITAR TAG -->
    <v-dialog
      v-model="editar_tag"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="#4b779e">
          <v-btn icon dark @click="editar_tag = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Editar Tag</v-toolbar-title>
        </v-toolbar>

        <v-container v-if="tag_escolhida_editar != ''">
          <v-row>
            <v-col cols="6">
              <v-row>
                <v-text-field
                  v-model="tag_nome"
                  disabled
                  label="Nome da tag"
                  required
                ></v-text-field>
              </v-row>
              <v-row>
                <v-radio-group v-model="tag_isAtiva" flat row>
                  <v-radio label="Ativa" :value="true"></v-radio>
                  <v-radio label="Inativa" :value="false"></v-radio>
                </v-radio-group>
              </v-row>
            </v-col>
            <v-col cols="2"></v-col>
            <v-col cols="4">
              <v-color-picker
                class="ma-2"
                v-model="tag_color"
                disabled
                hide-canvas
                hide-inputs
                show-swatches
              ></v-color-picker>
            </v-col>
          </v-row>
          <v-row v-if="tag_nome != 'localidade'">
            <v-combobox
              v-model="tag_dicionario"
              label="Dicionário"
              multiple
              chips
              deletable-chips
              outlined
            ></v-combobox>
          </v-row>
          <v-row>
            <v-combobox
              v-model="tag_indicadores"
              label="Indicadores de Início de Classe"
              multiple
              chips
              deletable-chips
              outlined
            ></v-combobox>
          </v-row>

          <v-row>
            <v-spacer />
            <v-btn class="ma-2" color="#4b779e" dark @click="saveTag()"
              >Guardar</v-btn
            >
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>

    <!-- REMOVER TAG -->
    <v-dialog v-model="dialog_remove_tag" width="500">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title
          >Remover Tag</v-card-title
        >
        <v-card-text>
          <h3>Tem a certeza que pretende remover a tag ?</h3>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog_remove_tag = false"
            >Fechar</v-btn
          >
          <v-btn color="primary" text @click="removeTag()">Remover</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- DIALOG ERRO -->
    <v-dialog v-model="error_dialog" width="500">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title
          >ERRO</v-card-title
        >
        <v-card-text>
          <v-row>
            <h4>{{ error_dialog_message }}</h4>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog_nova_regra = false"
            >Fechar</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>



<script>
import axios from "axios";
import NovaTagComponent from "@/components/tagging/NovaTagComponent.vue";
const lhost = 'https://tommi2.di.uminho.pt/api'
//const lhost = "http://localhost:5000";

export default {
  components: {
    NovaTagComponent,
  },
  data() {
    return {
      // Lista de Tags
      headers: [
        {
          text: `${this.$t("tagging.nome")}`,
          align: "start",
          value: "_id",
        },
        {
          text: `${this.$t("tagging.atividade")}`,
          value: "atividade",
        },
        {
          text: `${this.$t("tagging.cor")}`,
          value: "cor",
        },
        {
          text: `${this.$t("def.opt")}`,
          value: "options",
          sortable: false,
        },
      ],
      search: "",
      tags: [],

      //Dialog editar
      editar_tag: false,
      error_dialog: false,
      error_dialog_message: "",
      tags_ativas: [],
      tags_ativas_info: {},
      indicadoresStop_list: [],
      tag_escolhida_editar: "",

      tag_nome: "",
      tag_color: "",
      tag_isAtiva: "",
      tag_dicionario: [],
      tag_indicadores: [],

      //Dialog remover
      dialog_remove_tag: false,
      tag_escolhida_remover: {},
    };
  },
  methods: {
    onUpdate() {
      axios
        .get(lhost + "/tagging/tagsAtivas")
        .then((response) => {
          this.tags = response.data.list_tags;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    openEditDialog: async function (item) {
      this.tag_escolhida_editar = item.tag;
      this.getInfoTag();
      this.editar_tag = true;
    },
    openRemoveDialog: async function (item) {
      this.tag_escolhida_remover = item;
      this.dialog_remove_tag = true;
    },
    getInfoTag: async function () {
      if (this.tag_escolhida_editar != "") {
        try {
          var tag_info_response = await axios.get(
            lhost + "/tagging/infoTag/" + this.tag_escolhida_editar
          );
          var info_tag = tag_info_response.data.info_tag;
          this.tag_nome = info_tag.tag;
          this.tag_color = info_tag.cor;
          this.tag_isAtiva = info_tag.ativa;
          this.tag_dicionario = info_tag.dicionario;
          this.tag_indicadores = info_tag.start;
        } catch (e) {
          return e;
        }
      }
    },
    removeTag: async function () {
      this.dialog_remove_tag = false;
      axios
        .post(lhost + "/tagging/tags/remove", {
          tag: this.tag_escolhida_remover,
        })
        .then(() => {
          this.tag_escolhida_remover = {};
          this.onUpdate();
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    refresh: function () {
      this.onUpdate();
    },
    saveTag: async function () {
      if (
        this.validateName() &&
        this.validateIsActiva() &&
        this.validateColor()
      ) {
        var editTag = {};
        editTag["ativa"] = this.tag_isAtiva;
        editTag["cor"] = this.tag_color;
        editTag["dicionario"] = this.tag_dicionario;
        editTag["start"] = this.tag_indicadores;
        axios
          .post(lhost + "/tagging/tags/edit", {
            id: this.tag_nome,
            tag: editTag,
          })
          .then(() => {
            this.editar_tag = false;
            this.refresh
            this.tag_nome = "";
            this.tag_color = "";
            this.tag_isAtiva = "";
            this.tag_dicionario = [];
            this.tag_indicadores = [];
          })
          .catch((e) => {
            this.errors.push(e);
          });
      }
    },
    validateName: function () {
      for (var tag in this.tags_ativas) {
        if (this.tag_nome == tag) {
          this.error_dialog = true;
          this.error_dialog_message = "Já existe uma tag com esse nome!";
          return false;
        }
      }
      return true;
    },
    validateIsActiva: function () {
      if (this.tag_isAtiva == "") {
        this.error_dialog = true;
        this.error_dialog_message = "Indique se a tag é ativa!";
        return false;
      }
      return true;
    },
    validateColor: function () {
      if (this.tag_color == "") {
        this.error_dialog = true;
        this.error_dialog_message = "Selecione uma cor para a tag";
        return false;
      }
      return true;
    }
  },
  created() {
    this.onUpdate();
  }
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
