<template>
  <v-container>
    <v-row>
      <v-col>
        <h4>Sistema de Anotação Automática de Textos</h4>
      </v-col>
    </v-row>
    <hr />

    <v-row>
      <!-- Menu Column 1 - Words Agregator  -->
      <v-col cols="6">
        <v-container>
          <v-row>
            <h6>Agregador de Palavras</h6>
          </v-row>

          <v-row>
            <v-select
              color="#003366"
              :disabled="agregador_desativa_opt"
              dense
              :items="tags"
              label="Escolher Tag"
              v-model="tag_escolhida"
              outlined
            ></v-select>
          </v-row>

          <v-row>
            <v-spacer />
            <v-radio-group :disabled="agregador_desativa_opt" v-model="row" flat row>
              <v-radio label="Individual" value="radio-1"></v-radio>
              <v-radio label="Texto" value="radio-2"></v-radio>
            </v-radio-group>
            <v-spacer />
          </v-row>

          <v-row>
            <v-spacer />
            <v-btn
              color="#003366"
              dark
              class="ma-2"
              :disabled="agregador_desativa_opt"
              @click="validarTag()"
            >Validar</v-btn>
            <v-spacer />
            <v-dialog v-model="agregador_dialog_validar" persistent max-width="500">
              <v-card>
                <v-card-title class="font-header">Erro!</v-card-title>
                <v-card-text>
                  <h3>{{agregador_message_validar}}</h3>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="agregador_dialog_validar = false">Fechar</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </v-container>
      </v-col>

      <v-col cols="4">
      </v-col>

      <!-- Menu Column 2 - Submeter -->
      <v-col cols="2">
        <v-container>
          <!-- Menu Column 1 - Line 1 -->
          <v-row>
            <v-switch color="#003366" dense v-model="mostrar_tags" label="Mostrar Tags"></v-switch>
          </v-row>
          
          <!-- Menu Column 1 - Line 2 -->
          <v-row>
            <v-btn class="ma-2 border-bottom" color="#003366" @click="guardarFolio()" dark>Submeter</v-btn>
          </v-row>
        </v-container>
      </v-col>
    </v-row>

    <!-- Folio Editor -->
    <v-row>
      <v-col cols="12">
        <h5>Fólio</h5>
        <hr />
        <div style="max-height: 200px; overflow: scroll;">
          <!-- Folio: Word by word -->
          <span v-for="word in textoAnotado" :key="word">
            <template v-if="mostrar_tags == false && word.anotated == true">
              <v-tooltip top>
                <template v-slot:activator="{ on }">
                  <span>
                    <a
                      :style="{ color: word.color }"
                      v-on="on"
                      @click="openTagEditor(word)"
                    >{{ word.s_tag }}</a>
                  </span>
                </template>
                <span>{{word.tipo}}</span>
              </v-tooltip>
            </template>

            <template
              v-else-if="mostrar_tags == false && word.anotated == false && word.selected == true"
            >
              <span class="black">
                <a :style="{ color: 'white' }" @click="openTagEditor(word)">{{ word.word }}</a>
              </span>
            </template>

            <template
              v-else-if="mostrar_tags == true && word.anotated == false && word.selected == true"
            >
              <span class="black">
                <a :style="{ color: 'white' }" @click="openTagEditor(word)">{{ word.word }}</a>
              </span>
            </template>

            <template v-else>
              <template v-if="word.anotated==true">
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <span>
                      <a
                        :style="{ color: word.color }"
                        v-on="on"
                        @click="openTagEditor(word)"
                      >{{ word.word }}</a>
                    </span>
                  </template>
                  <span>{{word.tipo}}</span>
                </v-tooltip>
              </template>
              <template v-else>
                <span>
                  <a
                    :style="{ color: word.color }"
                    v-on="on"
                    @click.exact="openTagEditor(word)"
                  >{{ word.word }}</a>
                </span>
              </template>
            </template>

            <!-- Folio: Need to put a space between-->
            <span>{{word_space}}</span>
          </span>

          <!-- Word: Pop-up Editor-->
          <v-dialog v-model="tag_editor" width="500" persistent>
            <v-card>
              <template v-if="choosen_word.anotated==true">
                <v-card-title class="headline grey lighten-2" primary-title>{{choosen_word.s_tag}}</v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-spacer />
                      <v-tooltip top>
                        <template v-slot:activator="{ on }">
                          <v-btn v-on="on" class="ma-2" @click="tag_editor_option = 1">
                            <v-icon>mdi-pencil</v-icon>
                          </v-btn>
                        </template>
                        <span>Editar Tag</span>
                      </v-tooltip>

                      <v-tooltip top>
                        <template v-slot:activator="{ on }">
                          <v-btn v-on="on" class="ma-2" @click="tag_editor_option = 2">
                            <v-icon>mdi-delete</v-icon>
                          </v-btn>
                        </template>
                        <span>Apagar Tag</span>
                      </v-tooltip>
                      <v-spacer />
                    </v-row>
                  </v-container>

                  <!-- Word Anotated: Edit Tag-->
                  <v-container v-if="tag_editor_option == 1">
                    <v-row>
                      <v-select
                        dense
                        :items="tags"
                        label="Nova Tag"
                        v-model="tag_escolhida_editar"
                        outlined
                      ></v-select>
                    </v-row>
                    <v-row
                      v-if="tag_escolhida_editar != '' && tag_escolhida_editar != choosen_word.tipo"
                    >
                      <v-spacer />
                      <v-btn class="mx-2" @click="validarEditar(choosen_word)">Validar</v-btn>
                      <v-spacer />
                    </v-row>
                  </v-container>

                  <!-- Word Anotated: Remove Tag-->
                  <v-container v-if="tag_editor_option == 2">
                    <hr>
                    <v-row>
                      <v-spacer></v-spacer>
                      <v-radio-group flat row>
                        <v-radio label="Individual" value="radio-1"></v-radio>
                        <v-radio label="Todas" value="radio-2"></v-radio>
                      </v-radio-group>
                      <v-spacer></v-spacer>
                    </v-row>
                    <v-row>
                      <v-spacer />
                      <v-btn dark color="red" class="mx-2" @click="tag_editor_option_apagar = true">Apagar</v-btn>
                      <v-spacer />
                    </v-row>
                  </v-container>

                </v-card-text>
              </template>

              <template v-if="choosen_word.anotated==false && choosen_word.selected == false">
                <v-card-title class="headline grey lighten-2" primary-title>{{choosen_word.s_tag}}</v-card-title>

                <v-card-text>
                  <v-row>
                    <v-spacer />
                    <v-tooltip top>
                      <template v-slot:activator="{ on }">
                        <v-btn v-on="on" class="ma-2" @click="adicionaPal(choosen_word)">
                          <v-icon>mdi-plus</v-icon>
                        </v-btn>
                      </template>
                      <span>Adicionar a Agregador</span>
                    </v-tooltip>
                    <v-spacer />
                  </v-row>
                </v-card-text>
              </template>

              <template v-if="choosen_word.anotated==false && choosen_word.selected == true">
                <v-card-title class="headline grey lighten-2" primary-title>{{choosen_word.s_tag}}</v-card-title>

                <v-card-text>
                  <v-row>
                    <v-spacer />
                    <v-tooltip top>
                      <template v-slot:activator="{ on }">
                        <v-btn v-on="on" class="ma-2" @click="removePal(choosen_word)">
                          <v-icon>mdi-close</v-icon>
                        </v-btn>
                      </template>
                      <span>Retirar do Agregador</span>
                    </v-tooltip>
                    <v-spacer />
                  </v-row>
                </v-card-text>
              </template>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="closeEditor()">Fechar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-dialog v-model="tag_editor_option_apagar" max-width="500">
            <v-card>
              <v-card-title class="font-header">{{choosen_word.word}}</v-card-title>
              <v-card-text>
                <h3>Tem a certeza que pretende apagar a Tag ?</h3>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="tag_editor_option_apagar = false">Cancelar</v-btn>
                <v-btn color="red darken-1" text @click="removeTag(choosen_word)">Apagar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
      </v-col>
    </v-row>

    <br />
    <hr />
  </v-container>
</template>

<script>
import axios from "axios";
const lhost = 'https://tommi2.di.uminho.pt/api'
//const lhost = "http://localhost:5000";

export default {
  name: "EditorComponent",
  components: {
  },
  data: () => ({
    // Global
    tags: [],
    info_tags: {},

    // Menu - column 1
    mostrar_tags: true,
    relacoes_tags: false,

    // Menu - column 2
    agregador_adicionarTagList: {},
    agregador_dialog_validar: false,
    agregador_message_validar: "",
    agregador_desativa_opt: true,
    agregador_size: 0,
    tag_escolhida: "",

    // Folio
    textoAnotado: [],
    idTextoAnotado: [],
    word_space: " ",

    // Word Menu
    choosen_word: {},
    tag_editor: false,
    tag_escolhida_editar: "",
    tag_editor_option: 0,
    tag_editor_option_editar: false,
    tag_editor_option_apagar: false
  }),
  mounted: async function() {
    try {
      this.textoAnotado = this.$store.getters.currentTextoAnotado;
      this.idTextoAnotado = this.$store.getters.currentIdTextoAnotado;
    } catch (e) {
      return e;
    }
  },
  methods: {
    removeTag: function(word) {
      var split_word = word.s_tag.split(" ");
      for (var i = 0; i < split_word.length; i++) {
        var tmp = {};
        var position = word.position + i;
        tmp["word"] = split_word[i];
        tmp["s_tag"] = split_word[i];
        tmp["position"] = position;
        tmp["anotated"] = false;
        tmp["tipo"] = "";
        tmp["color"] = "black";
        tmp["selected"] = false;
        if (i == 0) {
          this.textoAnotado.splice(position, 1, tmp);
        } else {
          this.textoAnotado.splice(position, 0, tmp);
        }
      }
      for (i = 0; i < this.textoAnotado.length; i++) {
        this.textoAnotado[i].position = i;
      }
      this.tag_editor_option_apagar = false;
      this.tag_editor_option = 0;
      this.tag_editor = false;
    },
    removePal: function(word) {
      word.selected = false;
      delete this.agregador_adicionarTagList[word.position];
      this.agregador_size = this.agregador_size - 1;
      if (this.agregador_size == 0) {
        this.agregador_desativa_opt = true;
      }
      this.tag_editor = false;
    },
    adicionaPal: function(word) {
      word.selected = true;
      this.agregador_adicionarTagList[word.position] = word;
      this.agregador_size = this.agregador_size + 1;
      this.agregador_desativa_opt = false;
      this.tag_editor = false;
    },
    validarTag: function() {
      if (this.tag_escolhida == "") {
        this.agregador_message_validar =
          "Não escolheu nenhuma tag para validar!";
        this.agregador_dialog_validar = true;
      } else {
        var parar = false;
        var all_keys = Object.keys(this.agregador_adicionarTagList);
        all_keys = all_keys.sort();

        for (var i = 1; i < all_keys.length; i++) {
          if (all_keys[i] - all_keys[i - 1] != 1) {
            parar = true;
            this.agregador_message_validar =
              "As palavras não estão seguidas. Não pode haver interavlos entre as palavras!";
            this.agregador_dialog_validar = true;
          }
        }
        if (parar == false) {
          var tmp = {};
          tmp["word"] = "";
          tmp["s_tag"] = "";
          tmp["position"] = all_keys[0];
          tmp["anotated"] = true;
          tmp["tipo"] = this.tag_escolhida;
          tmp["color"] = this.info_tags[this.tag_escolhida].cor;
          tmp["selected"] = false;

          var tag_word = "<" + this.tag_escolhida + "> ";
          var s_tag = "";
          for (i = 0; i < all_keys.length; i++) {
            var tmp_word = this.agregador_adicionarTagList[all_keys[i]].word;
            tag_word = tag_word + " " + tmp_word;
            if (i == 0) {
              s_tag = tmp_word;
            } else {
              s_tag = s_tag + " " + tmp_word;
            }
          }
          tag_word = tag_word + " </" + this.tag_escolhida + ">";
          tmp["word"] = tag_word;
          tmp["s_tag"] = s_tag;
          this.textoAnotado.splice(tmp["position"], all_keys.length, tmp);

          for (i = 0; i < this.textoAnotado.length; i++) {
            this.textoAnotado[i].position = i;
          }

          this.agregador_adicionarTagList = {};
          this.tag_escolhida = "";
          this.agregador_size = 0;
          this.agregador_desativa_opt = true;
        }
        this.tag_editor=false;
      }
    },
    validarEditar: function(word) {
      var tag_word =
        "<" +
        this.tag_escolhida_editar +
        "> " +
        word.s_tag +
        " </" +
        this.tag_escolhida_editar +
        ">";
      word.word = tag_word;
      word.tipo = this.tag_escolhida_editar;
      word.color = this.info_tags[this.tag_escolhida_editar].cor;
      this.tag_escolhida_editar = "";
      this.dialog_editar = false;
      this.tag_editor_option_editar = false;
      this.tag_editor_option = 0;
      this.tag_editor = false;
    },
    openTagEditor: function(word) {
      this.choosen_word = word;
      this.tag_editor = true;
    },
    closeEditor: function() {
      this.tag_editor = false;
      this.tag_editor_option = 0;
    },
    guardarFolio: function () {
      axios
        .post(lhost + "/tagging/folio/guardar", {id: this.idTextoAnotado, words: this.textoAnotado})
        .then(() => {
          this.$router.push("/admin/tagging");
        })
        .catch((e) => {
          this.errors.push(e);
        });
    }
  }
};
</script>
