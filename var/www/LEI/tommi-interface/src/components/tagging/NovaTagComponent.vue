<template>
  <v-container>
    <v-tooltip top>
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          class="ma-2"
          color="#4b779e"
          @click="nova_tag = true"
          dark
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </template>
      <span>Nova Tag</span>
    </v-tooltip>

    <v-dialog
      v-model="nova_tag"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="#4b779e">
          <v-btn icon dark @click="nova_tag = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Nova Tag</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items> </v-toolbar-items>
        </v-toolbar>

        <v-container>
          <v-row>
            <v-col cols="6">
              <v-row>
                <v-text-field
                  v-model="tag_nome"
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
                v-model="tag_color"
                class="ma-2"
                disabled
                hide-canvas
                hide-inputs
                show-swatches
              ></v-color-picker>
            </v-col>
          </v-row>
          <v-row>
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
            <v-btn dark class="ma-2" color="#4b779e" @click="cleanAll()"
              >Limpar</v-btn
            >
            <v-btn dark class="ma-2" color="#4b779e" @click="saveTag()" 
              >Guardar</v-btn
            >
          </v-row>
          <br />
        </v-container>
      </v-card>
    </v-dialog>

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
  </v-container>
</template>


<script>
import axios from "axios";
const lhost = 'https://tommi2.di.uminho.pt/api'
//const lhost = "http://localhost:5000";


export default {
  name: "NovaTagComponent",
  data: () => ({
    nova_tag: false,
    tags_ativas: [],
    tags_ativas_info: {},
    error_dialog: false,
    error_dialog_message: "",

    //campos da tag
    tag_nome: "",
    tag_color: "",
    tag_isAtiva: "",
    tag_dicionario: [],
    tag_indicadores: [],

  }),
  mounted: async function () {
    try {
      var info_response = await axios.get(lhost + "/tagging/tagsAtivas");
      this.tags_ativas = info_response.data.tags;
      this.tags_ativas_info = info_response.data.info_tags;
    } catch (e) {
      return e;
    }
  },
  methods: {
    saveTag: async function () {
      if (
        this.validateName() &&
        this.validateIsActiva() &&
        this.validateColor()
      ) {
        var novaTag = {};
        novaTag["tag"] = this.tag_nome;
        novaTag["ativa"] = this.tag_isAtiva;
        novaTag["cor"] = this.tag_color;
        novaTag["dicionario"] = this.tag_dicionario;
        novaTag["start"] = this.tag_indicadores
        axios
        .post(lhost + "/tagging/tags/adiciona", {nova_tag: novaTag})
        .then(() => {
          this.nova_tag = false
          this.tag_nome = ""
          this.tag_color =  ""
          this.tag_isAtiva =  ""
          this.tag_dicionario = []
          this.tag_indicadores = []
          this.$emit('listChanged')
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
};
</script>