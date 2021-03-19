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
      id="tabelaFolios"
      :headers="headers"
      :items="folios"
      :items-per-page="15"
      :sort-by="['_id']"
    >
      <template v-slot:header._id="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.descricao="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.versao="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.sumario="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.tipo="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.ver="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:item.ver="{ item }">
        <template v-if="isAnotado(item._id)">
          <v-icon small class="mr-2" @click="verFolio(item._id)"> mdi-eye </v-icon>
        </template>
        <template v-if="isAtualizado(item._id)">
          <v-icon small class="mr-2" @click="verFolioAtualizado(item._id)"> mdi-mail </v-icon>
        </template>
      </template>
      <template v-slot:header.anotar="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:item.anotar="{ item }">
        <v-icon small class="mr-2" @click="anotarFolio(item)">
          mdi-pencil
        </v-icon>
        <v-icon small class="mr-2" @click="atualizarFolio(item)">
          mdi-update
        </v-icon>
      </template>
    </v-data-table>
  </div>
</template>



<script>
import axios from "axios";
const lhost = 'https://tommi2.di.uminho.pt/api'
//const lhost = "http://localhost:5000";

export default {
  data() {
    return {
      headers: [
        {
          text: `${this.$t("fol.id")}`,
          align: "start",
          value: "_id",
        },
        {
          text: `${this.$t("fol.desc")}`,
          value: "descricao",
        },
        {
          text: `${this.$t("fol.versao")}`,
          value: "versao",
        },
        {
          text: `${this.$t("fol.sum")}`,
          value: "sumario",
        },
        {
          text: `${this.$t("fol.tipo")}`,
          value: "tipo",
        },
        {
          text: `${this.$t("tagging.ver")}`,
          value: "ver",
          sortable: false,
        },
        {
          text: `${this.$t("tagging.anotar")}`,
          value: "anotar",
          sortable: false,
        },
      ],
      folios: [],
      errors: [],
      item: {},

      listaFoliosAnotados:[],
      listaFoliosAtualizados:[],
    };
  },
  created() {
    axios
      .get(
        `https://tommi2.di.uminho.pt/api/folios/folios?nome=${this.$store.state.user._id}`,
        {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        }
      )
      .then((response) => {
        this.folios = response.data.folios;
        axios
        .get(lhost + "/tagging/folio/foliosAnotados")
        .then((response) => {
          this.listaFoliosAnotados = response.data.listaFoliosAnotados;
          axios
          .get(lhost + "/tagging/folio/foliosAtualizados")
          .then((response) => {
            this.listaFoliosAtualizados = response.data.listaFoliosAtualizados;
          })
          .catch((e) => {
            this.errors.push(e);
        });

        })
        .catch((e) => {
          this.errors.push(e);
        });
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
  methods: {
    anotarFolio(item) {
      axios
        .post(lhost + "/tagging/submeterFolio", {folio: item.textoSTags})
        .then((texto_anotado) => {
          this.$store.commit("updateTextoAnotado", texto_anotado.data.texto);
          this.$store.commit("updateIdTextoAnotado", item._id);
          this.redirecionar();
        })
        .catch((err) => alert(err));
    },
    atualizarFolio(item) {
      axios
        .get(lhost + "/tagging/atualizarFolio/" + item._id)
        .then((textoAtualizado) => {
          this.$store.commit("updateTextoAtualizado", textoAtualizado.data.texto);
          this.$store.commit("updateIdTextoAtualizado", item._id);
          this.$store.commit("updateReplacerList", textoAtualizado.data.replacerList);
          this.$router.push("/admin/tagging/modernizador");
        })
        .catch((err) => alert(err));
    },
    redirecionar() {
      this.$router.push("/admin/tagging/editor");
    },
    isAnotado(item){
      if(this.listaFoliosAnotados.includes(item)){
        return true
      }else{return false;}
    
    },
    isAtualizado(item){
      if(this.listaFoliosAtualizados.includes(item)){
        return true
      }else{return false;}
    
    },
    verFolio(id){
      this.$router.push("/admin/tagging/folioAnotado/ver/" + id);
    },
    verFolioAtualizado(id){
      this.$router.push("/admin/tagging/folioAtualizado/ver/" + id);
    }
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
  color: #73879C;
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
