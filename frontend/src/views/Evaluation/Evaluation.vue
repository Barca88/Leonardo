<template>
  <v-container class="pa-10">
    <AppHeader></AppHeader>
    <NavDraw></NavDraw>
    <h3 class="text-h3 grey--text text--lighten-1 mb-5">
      Realizacao de testes
    </h3>

    <h4 class="text-h4 mb-4">Escolha o Dominio</h4>

    <DomainForm v-model="domain" />
  
    <v-expand-transition>
      <v-data-table
        v-show="domain != null"
        ref="table"
        :items="tableTests"
        :sort-by="['_id']"
        :headers="headers"
        :items-per-page="15"
        :search="search"
        multi-sort
      >
        <template v-slot:top>
          <!-- Heading for mobile -->
          <h5 class="text-h5 px-4 hidden-md-and-up">Gestao de Testes</h5>
          <v-divider class="mx-2 hidden-md-and-up" />

          <v-toolbar flat color="white">
            <!-- Heading for larger screens -->
            <v-toolbar-title class="hidden-sm-and-down">
              Escolha de Teste
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
          </v-toolbar>
        </template>

        <template v-slot:[`item.options`]="{ item }">
          <div class="d-flex">
            <v-btn small text link :to="`/evaluation/${item._id}`" class="mx-1">
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn text small class="warning--text change-font" v-on="on">
                    <v-icon v-text="'mdi-pen'" />
                  </v-btn>
                </template>
                <span>Realizar</span>
              </v-tooltip>
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-expand-transition>

    <TextSnackBar
      :color="snackbar.color"
      :text="snackbar.text"
      :show="snackbar.show"
      @close="snackbar.show = false"
    />

    <Footer class="mt-5"></Footer>
  </v-container>
</template>

<script>
import AppHeader from '@/components/header.vue'
import NavDraw from '@/components/navDraw'
import Footer from '@/components/Footer'
import DomainForm from '@/components/Evaluation/DomainForm'
import TextSnackBar from '@/components/UI/TextSnackBar'
import axios from 'axios'
import * as testsApi from '@/utils/api/tests'


export default {
  name: 'Evaluation',
  components: {
    TextSnackBar,
    DomainForm,
    AppHeader,
    NavDraw,
    Footer
  },
  data() {
    return {
      domain: null,
      loading: true,
      search: '',
      Domain: [],
      idDomain: [],
      tests: [],
      headers: [
        {
          text: 'Identificador',
          value: '_id'
        },
        {
          text: 'Descrição',
          value: 'description'
        },
        {
          text: 'Dominio',
          value: 'domain'
        },
        {
          text: 'SubDominios',
          value: 'subdomains'
        },
        {
          text: 'Autor',
          value: 'inserted_by'
        },
        {
          text: 'Ultima Atualizacao',
          value: 'last_updated'
        },
        {
          text: 'Opções',
          value: 'options',
          sortable: false
        }
      ],
      snackbar: {
        show: false,
        text: '',
        color: ''
      }
    }
  },
  methods: {
    snackbarFetchFailed() {
      this.snackbar = {
        show: true,
        color: 'error',
        text: `O servidor não conseguiu obter a informação sobre os dominios !! ☹ \n`
      }
    }
  },

  computed: {
    
    /** @return {any} */
    tableTests() {
      if (this.domain != null) {
        return this.tests
          .filter(
            (t) =>
              t.config.domain === this.domain
          )
          .map((t) => ({
            ...t.config,
            subdomains: t.config.subdomains.join(', '),
            domain: t.config.domain.description,
            _id: t._id
          }))
      } else return []
    },
    tableTests1() {
      return this.tests.map((t) => ({
        ...t.config,
        subdomains: t.config.subdomains.join(', '),
        domain: t.config.domain,
        _id: t._id
      }))
    }
  },

  created() {
    this.loading = true
     axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions`,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': "*"    
          },
        })
      .then((response)=>{
        response.data.domains.forEach((obj) =>{
          console.log('found something')
          this.Domain.push(obj)
          this.idDomain.push(obj._id)
        });
      },(error) =>{
          console.log(error);
    });
    testsApi
        .getAll()
        .then((data) => {
          this.tests = data.tests
          console.log('received -' + this.tests[0])
          this.loading = false
        })
        .catch(() => {
          this.snackbar = {
            show: true,
            color: 'error',
            text: `Não foi possivel obter a lista de testes !! 😫 \n`
          }
        })
  }
}
</script>

<style scoped>
.container {
  margin: 20px auto 80px auto;
  max-width: 1100px;
}

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
