<template>
  <v-container class="pa-10">
    <AppHeader></AppHeader>
    <NavDraw></NavDraw>
    <section>
      <h4 class="text-h4 mb-4">Selecao de Dominio</h4>

      <!-- Dominio -->
      <v-select
        :value="domain"
        :items="this.idDomain"
        :label="`${$t('title.chooseDomain')}`"
        @change="onChange($event)"
        @input="emitChange('domain', $event)"
        clearable
      />
      <!-- SubDominios -->
      <v-select
        :items="this.idSubDomain"
        :value="this.subdomains"
        :label="`${$t('title.chooseSubDomain')}`"
        @input="onChangeSub($event)"
        @change='subchange()'
        multiple
        chips
        deletable-chips
      />

    </section>


    <v-tooltip top v-if="step>1">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-on="on"
                  @click="fetchResults()"
                  v-bind="attrs"
                  class="blue-grey darken-4 white--text mx-2"
                >
                  <v-icon small v-text="'mdi-file-plus-outline'" />
                </v-btn>
              </template>
              <span>Mostrar</span>
        </v-tooltip>
        

        <v-expand-transition>
      <v-data-table v-if="step==3"
        v-show="domain != null"
        ref="table"
        :items="this.tests"
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

           
          </v-toolbar>
        </template>
        <template v-slot:[`item.options`]="{ item }">
          <div class="d-flex">
            <v-btn small text link :to="`/individualResult/${item.testId + item.student_id}`" class="mx-1">
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

    <Footer class="mt-5"></Footer>
  </v-container>
</template>

<script>
//import axios from 'axios'
import AppHeader from '@/components/header.vue'
import NavDraw from '@/components/navDraw'
import Footer from '@/components/Footer'
import axios from 'axios';

export default {
  name: 'Preparation',
  components: {
    AppHeader,
    NavDraw,
    Footer
  },
  data() {
    return {
      sendObject:{
        sendId:'',
        sendDomain: '',
        sendHeader: '',
      },
      //1->config, 2->select questions
      step: 1,
      domain:{},
      idDomain: [],
      Domain: [],
      tests: [],
      subdomains: [],
      loading: true,
      testConfigs: {},
      allTests:[],
      testItemsChosen: [],
      testItems:[],
      test: null,
      testStore:null,
      questionUpdates: {
        replacingQuestions: [],
        replacedQuestions: [],
        notReplacedQuestions: 999
      },
       headers: [
        {
          text: 'Teste',
          value: 'testId'
        },
        {
          text: 'Estudante',
          value: 'student_id'
        },
        {
          text: 'Resultado ( Percentagem )',
          value: 'result'
        },
        {
          text: 'Número de Perguntas',
          value: 'questions.length'
        },
        {
          text: 'SubDominios',
          value: 'config.subdomains'
        },
        {
          text: 'Opções',
          value: 'options',
          sortable: false
        }
      ],
      resetCounter: 0,
      showTestDisplayDialog: false,
      snackbar: {
        show: false,
        text: '',
        color: ''
      }
    }
  },
  methods: {
    onDomain(){
      if(this.sendObject.sendDomain != this.domain){
        this.idSubDomain = []
        if(this.domain){
          this.Domain.forEach((obj) =>{
            if(obj._id == this.domain){
              obj.body.forEach((sub) =>{
                this.idSubDomain.push(sub.subdomain)
              });
            }
          });
        }
      }
    },
    onChangeTest(e){
      this.testItemsChosen = e
    },
    onChangeSub(e){
      this.subdomains = e
      this.testChanges()
    },
    testChanges(){
      this.testItems = []
      
      this.allTests.forEach((test) =>{
            if(test['config']['domain'] == this.domain){
              if(this.subdomains == '')
                this.testItems.push(test['_id'])
              else{
                test['config']['subdomains'].forEach((sub) =>{
                  if(this.subdomains.includes(sub))
                    this.testItems.push(test['_id'])
                })

              }
            }
          })
    },

    onChange(e){
      this.step=2
      this.domain = e
      this.sendObject.sendId = this.selectedDomain
      this.onDomain()
      this.sendObject.sendDomain = this.domain
      this.sendObject.sendHeader = this.headerobj
      //this.$root.$emit('change',this.sendObject)


      this.testChanges()

      
    },
    async fetchResults(){
      this.tests = []
      let formData = new FormData()
      formData.append('domain',this.domain)
      formData.append('subdomains', this.subdomains)
      formData.append('tests', this.testItemsChosen)
      formData.append('student', this.$store.state.user.studentNumber )
      await axios.post(`${process.env.VUE_APP_BACKEND}/tests/results`,formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': "*"    
          },
        })
      .then((response)=>{
        response.data.tests.forEach((obj) =>{
          this.tests.push(obj)
        });
      },(error) =>{
          console.log(error);
    });

    this.step=3


    }

  },

  async created() {
    try{
      this.testConfigs.subdomains.forEach((obj)=>{
        this.idSubDomain.push(obj)
        this.showNext = true
      })}
      catch( e ){console.log('')}
    //this.fetchDomains()
    axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions`,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': "*"    
          },
        })
      .then((response)=>{
        response.data.domains.forEach((obj) =>{
          this.Domain.push(obj)
          this.idDomain.push(obj._id)
        });
      },(error) =>{
          console.log(error);
    });
    const configDomain = this.testConfigs.domain
    //TODO Domains need Human Readable Ids
    if (configDomain)
      this.selectedDomain = `${configDomain.study_cycle}-${configDomain.scholarity}-${configDomain.description}`


      
  },

  watch: {
    '$route.query'() {
      this.clearFields()
      this.setInitialFields()
    }
  }
}
</script>

<style scoped>
.container {
  margin: 20px auto 80px auto;
  max-width: 1100px;
}
</style>
