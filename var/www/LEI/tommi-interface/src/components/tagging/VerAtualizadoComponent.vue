<template>
  <v-container>
    <v-row>
      <v-col>
        <h4>Sistema de Anotação Automática de Textos</h4>
      </v-col>
    </v-row>
    <hr />

    <!-- Folio Editor -->
    
      <v-row>
        <v-col cols="12">
          <h5>Fólio: {{idTextoAtualizado}}</h5>
          <hr />
          <div>
            <p>{{ textoAtualizado }}</p>
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
  name: "VerAtualizadoComponent",
  components: {},
  data: () => ({
    // Folio
    textoAtualizado: [],
    idTextoAtualizado: "",
  }),
  mounted: async function () {
    try {
      axios
        .get(
          lhost + "/tagging/folio/foliosAtualizados/" + this.$route.params.id
        )
        .then((response) => {
          this.idTextoAtualizado = this.$route.params.id;
          this.textoAtualizado = response.data.textoAtualizado;
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
