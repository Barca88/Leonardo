<template>
  <v-container>
    <v-row>
      <v-col>
        <h4>Sistema de Anotação Automática de Textos</h4>
      </v-col>
    </v-row>
    <hr />

    <v-container>
      <v-row>
        <v-col cols="10"> </v-col>
        <v-col cols="2">
          <v-switch
            color="#003366"
            dense
            v-model="mostrar_tags"
            label="Mostrar Tags"
          ></v-switch>
        </v-col>
      </v-row>
    </v-container>

    <!-- Folio Editor -->
    <v-row>
      <v-col cols="12">
        <h5>Fólio</h5>
        <hr />
        <div>
          <!-- Folio: Word by word -->
          <span v-for="word in textoAnotado" :key="word">
            <template v-if="mostrar_tags == false && word.anotated == true">
              <v-tooltip top>
                <template v-slot:activator="{ on }">
                  <span>
                    <a :style="{ color: word.color }" v-on="on">{{
                      word.s_tag
                    }}</a>
                  </span>
                </template>
                <span>{{ word.tipo }}</span>
              </v-tooltip>
            </template>

            <template
              v-else-if="
                mostrar_tags == false &&
                word.anotated == false &&
                word.selected == true
              "
            >
              <span class="black">
                <a :style="{ color: 'white' }">{{ word.word }}</a>
              </span>
            </template>

            <template
              v-else-if="
                mostrar_tags == true &&
                word.anotated == false &&
                word.selected == true
              "
            >
              <span class="black">
                <a :style="{ color: 'white' }">{{ word.word }}</a>
              </span>
            </template>

            <template v-else>
              <template v-if="word.anotated == true">
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <span>
                      <a :style="{ color: word.color }" v-on="on">{{
                        word.word
                      }}</a>
                    </span>
                  </template>
                  <span>{{ word.tipo }}</span>
                </v-tooltip>
              </template>
              <template v-else>
                <span>
                  <a :style="{ color: word.color }" v-on="on">{{
                    word.word
                  }}</a>
                </span>
              </template>
            </template>

            <!-- Folio: Need to put a space between-->
            <span>{{ word_space }}</span>
          </span>
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
  name: "VerFolioComponent",
  components: {},
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
    tag_editor_option_apagar: false,
  }),
  mounted: async function () {
    try {
      axios
        .get(lhost + "/tagging/folio/foliosAnotados/" + this.$route.params.id)
        .then((response) => {
          this.textoAnotado = response.data.textoAnotado;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    } catch (e) {
      return e;
    }
  },
  methods: {},
};
</script>
