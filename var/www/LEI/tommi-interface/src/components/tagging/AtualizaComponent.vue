<template>
  <v-container>
    <v-row>
      <v-col>
        <h4>Sistema de Anotação Automática de Textos</h4>
      </v-col>
    </v-row>
    <hr />

    <v-row>
      <v-col cols="6">
      </v-col>

      <v-col cols="4">
      </v-col>

      <v-col cols="2">
        <v-container>
          <v-row>
            <v-btn class="ma-2 border-bottom" color="#003366" @click="guardarFolioModernizado()" dark>Submeter</v-btn>
          </v-row>
        </v-container>
      </v-col>
    </v-row>

    <!-- Folio Editor -->
    <v-row>
      <v-col cols="12">
        <h5>Fólio Modernizado</h5>
        <hr />
        <div>
          <p>{{textoAtualizado}}</p>
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
  name: "AtualizaComponent",
  components: {
  },
  data: () => ({
    // Folio
    textoAtualizado: "",
    idTextoAtualizado: "",
    replacerList:[]


  }),
  mounted: async function() {
    try {
      this.textoAtualizado = this.$store.getters.currentTextoAtualizado;
      this.idTextoAtualizado = this.$store.getters.currentIdTextoAtualizado;
      this.replacerList = this.$store.getters.currentReplacerList;

    } catch (e) {
      return e;
    }
  },
  methods: {
    guardarFolioModernizado: function () {
      axios
        .post(lhost + "/tagging/folioAtualizado/guardar", {id: this.idTextoAtualizado, texto: this.textoAtualizado, replacerList: this.replacerList})
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
