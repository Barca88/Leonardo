<template>
  <v-container>
    <v-row>
      <v-col>
        <h4>Sistema de Anotação Automática de Textos</h4>
      </v-col>
    </v-row>
    <hr />
    <v-container>
      <div v-if="anota == 0" style="text-center">
        <v-row>
          <v-col cols="2"> </v-col>
          <v-col cols="9">
            <h3>
              Tem a certeza que pretende re-anotar todos os fólios do sistema ?
            </h3>
          </v-col>
          <v-col cols="1"> </v-col>
        </v-row>
        <v-row>
          <v-col cols="4"> </v-col>
          <v-col cols="2">
            <v-btn
              class="ma-2 border-bottom"
              color="#003366"
              @click="voltar()"
              dark
              >Cancelar</v-btn
            >
          </v-col>
          <v-col cols="2">
            <v-btn
              class="ma-2 border-bottom"
              color="red"
              @click="anotaBase()"
              dark
              >Sim</v-btn
            >
          </v-col>
          <v-col cols="4"> </v-col>
        </v-row>
      </div>

      <div v-if="anota == 1">
        <v-row align="center" justify="center">
          <p>Aguarde o processamento dos Fólios</p>
          <v-col cols="12">
            <div style="min-height: 500px">
              <v-progress-linear
                indeterminate
                color="blue darken-2"
              ></v-progress-linear>
            </div>
          </v-col>
        </v-row>
      </div>

      <div v-if="anota == 2">
        <v-row>
          <v-col cols="4"> </v-col>
          <v-col cols="7">
            <h3>Foram anotados {{ sucesso }} fólios com sucesso!</h3>
          </v-col>
          <v-col cols="1"> </v-col>
        </v-row>
        <v-row>
          <v-col cols="5">
          </v-col>
          <v-col cols="5">
            <v-btn
              class="ma-2 border-bottom"
              color="#003366"
              @click="voltar()"
              dark
              >Voltar</v-btn
            >
          </v-col>
          <v-col cols="2">
          </v-col>
        </v-row>
      </div>
    </v-container>
  </v-container>
</template>




<script>
import axios from "axios";
const lhost = 'https://tommi2.di.uminho.pt/api'
//const lhost = "http://localhost:5000";
export default {
  data: () => ({
    anota: 0,
    sucesso: 0,
  }),
  mounted: async function () {},
  methods: {
    anotaBase: function () {
      this.anota = 1;
      axios
        .get(lhost + "/tagging/anotaBase")
        .then((response) => {
          this.sucesso = response.data.sucesso;
          this.anota = 2;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    voltar: function () {
      this.$router.push("/admin/tagging");
    },
  },
};
</script>
