<template>   
     <v-container class="my-5">
       <AppHeader></AppHeader>
        <div>
            <NavDraw></NavDraw>
        </div>
           <v-layout justify-center row wrap>
             <v-flex xs10 sm10 md9 lg9>
                <v-card color="#2A3F54" elevation="10">
                  <v-row >
                    <v-col cols="2" lg="2" xl="1">
                      <v-img src="@/assets/raccoon.png" max-width="80" class="mt-5 ml-5"></v-img>
                    </v-col>
                    <v-col>
                      <v-card-title class="yellow--text text--darken-2 text-h4 mr-5">{{ $t('title.prod') }}</v-card-title>
                      <v-card-subtitle class="white--text text-h5">{{ $t('title.defDom') }}</v-card-subtitle>
                    </v-col>
                  </v-row>
                </v-card>

                <v-card class="mt-2" elevation="10" >
                  <v-tabs v-model="tab"  show-arrows>
                    <v-tab v-for="item in items" :key="item.tab">
                     {{ item.tab }}
                    </v-tab>
                  </v-tabs>
                  <v-tabs-items v-model="tab">
                   <v-tab-item eager> 
                      <Dominio ref="dm" @newdataDominio="handleDataDominios($event)"/>
                   </v-tab-item>
                   <v-tab-item eager>
                      <Subdominios ref="sm" @newdataSubdominio="handleDataSubdominios($event)"/>
                   </v-tab-item>
                   <v-tab-item eager>
                      <Comportamento ref="cp" @newdataComportamento="handleDataComportamento($event)"/>
                   </v-tab-item>
                 </v-tabs-items>
              </v-card>
              
              <v-card class="mx-auto" >
                <v-row class="px-2 pb-2 ma-0 py-2" justify="space-between">
                  <v-btn-toggle v-model="formatting" multiple dense class="ml-5 mb-3">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">   
                        <v-btn v-bind="attrs" v-on="on" @click="confirmSubmit" color="#F0B62B" elevation="5" class="mr-2">
                          <v-icon color="white">mdi-checkbox-marked-outline</v-icon>
                        </v-btn>                     
                      </template>
                      <span>{{ $t('opc.confirm') }}</span>
                    </v-tooltip>

                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">    
                        <v-btn v-bind="attrs" v-on="on" color="white" elevation="5" class="mr-2" @click="startImport">
                          <v-icon color="black">mdi-import</v-icon>
                        </v-btn>                    
                      </template>
                      <span>{{ $t('opc.import') }}</span>
                    </v-tooltip>

                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">    
                        <v-btn v-bind="attrs" v-on="on" color="#29E898" elevation="5" @click="reset1">
                          <v-icon color="white">mdi-broom</v-icon>
                        </v-btn>                    
                      </template>
                      <span>{{ $t('opc.limpar') }}</span>
                    </v-tooltip>
                  </v-btn-toggle>

                  <v-btn-toggle v-model="alignment"
                    dense class="mr-5 mb-3">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">    
                        <v-btn v-bind="attrs" v-on="on" color="#2A3F54" class="mr-2" elevation="5" @click="help">
                          <v-icon color="white">mdi-help</v-icon>
                        </v-btn>                    
                      </template>
                      <span>{{ $t('opc.ajuda') }}</span>
                    </v-tooltip>

                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">    
                         <v-btn v-bind="attrs" v-on="on" to="/domain" color="#29E898" elevation="5" class="">
                          <v-icon color="white">mdi-door-open</v-icon>
                        </v-btn>                    
                      </template>
                      <span>{{ $t('opc.sair') }}</span>
                    </v-tooltip>
                  </v-btn-toggle>
                </v-row>
                <!-- Janela para Confirmação da Submissão -->
                <v-dialog v-model="openSubmit" max-width="500px">
                  <v-card>
                    <v-app-bar color="#2A3F54" >
                      <div class="d-flex align-center">
                        <h3 width="40" class="white--text">{{ $t('title.confSubm') }} </h3>
                      </div>
                    </v-app-bar>
                    <v-container>
                      <v-row>
                        <v-col cols="3">
                          <v-card class="ml-4 mt-1" color="white" flat height="100px" width="110px" >
                              <v-img src="@/assets/questionmark.png"/>
                          </v-card>
                        </v-col>
                        <v-col cols="9">
                          <h3 class="ml-5 mt-5">{{ $t('title.confDom') }}</h3>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-card-actions>
                      <v-container>
                          <v-row >
                            <v-col class="text-right">
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#F0B62B" @click="submit" elevation="5" class="mt-5 mr-3">
                                    <v-icon color="white">mdi-checkbox-marked-outline</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>{{ $t('opc.confirm') }}</span>
                              </v-tooltip>

                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#29E898" @click="closeSubmit" elevation="5" class="mt-5">
                                    <v-icon color="white">mdi-door-open</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>{{ $t('opc.sair') }}</span>
                              </v-tooltip>
                            </v-col>
                          </v-row>
                      </v-container>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!-- Janela de Submissão Bem-Sucedida -->
                 <v-dialog v-model="openConfirmSubmit" max-width="500px">
                  <v-card>
                    <v-app-bar color="#2A3F54" >
                      <div class="d-flex align-center">
                        <h3 width="40" class="white--text"> {{ $t('title.subDom') }}</h3>
                      </div>
                    </v-app-bar>
                    <v-container>
                      <v-row>
                        <v-col cols="3">
                          <v-card class="ml-4 mt-1" color="white" flat height="100px" width="110px" >
                              <v-img src="@/assets/check.png"/>
                          </v-card>
                        </v-col>
                        <v-col cols="9">
                          <h3 class="ml-5 mt-5">{{ $t('title.subDomSucc') }}</h3>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-card-actions>
                      <v-container>
                          <v-row >
                            <v-col class="text-right">
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#29E898" to="/domain" @click="closeConfirmSubmit" elevation="5" class="mt-5">
                                    <v-icon color="white">mdi-door-open</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>{{ $t('opc.sair') }}</span>
                              </v-tooltip>
                            </v-col>
                          </v-row>
                      </v-container>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!-- Janela de Erro na Submissão -->
                <v-dialog v-model="openError" max-width="500px">
                  <v-card>
                    <v-app-bar color="#2A3F54" >
                      <div class="d-flex align-center">
                        <h3 width="40" class="white--text">{{ $t('error.sub') }}</h3>
                      </div>
                    </v-app-bar>
                    <v-container>
                      <v-row>
                        <v-col cols="3">
                          <v-card class="ml-4 mt-1" color="white" flat height="100px" width="110px" >
                              <v-img src="@/assets/error.png"/>
                          </v-card>
                        </v-col>
                        <v-col cols="9">
                          <h3 class="ml-5 mt-5">{{ $t('error.subDom') }}</h3>
                          <h3 class="ml-5">{{ $t('error.fields') }}</h3>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-card-actions>
                      <v-container>
                          <v-row >
                            <v-col class="text-right">
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#29E898" @click="closeError" elevation="5" class="mt-5">
                                    <v-icon color="white">mdi-door-open</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>{{ $t('opc.sair') }}</span>
                              </v-tooltip>
                            </v-col>
                          </v-row>
                      </v-container>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!-- Janela de Import -->
                <v-dialog v-model="openImport" max-width="500px">
                  <v-card>
                    <v-app-bar color="#2A3F54" >
                      <div class="d-flex align-center">
                        <h3 width="40" class="white--text"> {{ $t('title.importDom') }}</h3>
                      </div>
                    </v-app-bar>
                    <v-container>
                      <v-row>
                        <v-col cols="9">
                          <h3 class="ml-5 mt-5">{{ $t('title.importDom2') }}</h3>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="9" class="ml-5">
                          <v-text-field v-model="idImport" 
                            :rules="[rules.required,...rules.repeatedID]"
                            label="Identificador"/>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-card-actions>
                      <v-container>
                          <v-row >
                            <v-col class="text-right">
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#F0B62B" @click="confirmImport" elevation="5" class="mt-5 mr-3">
                                    <v-icon color="white">mdi-import</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>{{ $t('opc.import') }}</span>
                              </v-tooltip>
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#29E898" @click="closeImport" elevation="5" class="mt-5">
                                    <v-icon color="white">mdi-door-open</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>{{ $t('opc.sair') }}</span>
                              </v-tooltip>
                            </v-col>
                          </v-row>
                      </v-container>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!-- Janela de Diálogo para Ajuda -->
                <v-dialog v-model="openHelp" max-width="500px">
                  <v-card>
                    <v-app-bar color="#2A3F54" >
                      <div class="d-flex align-center">
                        <h3 width="40" class="white--text">{{ $t('opc.ajuda') }}</h3>
                      </div>
                    </v-app-bar>
                    <v-container>
                      <v-row>
                        <v-col cols="3">
                          <v-card class="ml-4 mt-1" color="white" flat height="100px" width="110px" >
                              <v-img src="@/assets/information.png"/>
                          </v-card>
                        </v-col>
                        <v-col cols="9">
                          <h3 class="ml-5 mt-5">{{ $t('title.ajudaDom') }}</h3>
                          <h3 class="ml-5">{{ $t('title.ajuda2') }}</h3>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-card-actions>
                      <v-container>
                          <v-row >
                            <v-col class="text-right">
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#29E898" @click="closeHelp" elevation="5" class="mt-5">
                                    <v-icon color="white">mdi-door-open</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>{{ $t('opc.sair') }}</span>
                              </v-tooltip>
                            </v-col>
                          </v-row>
                      </v-container>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-card>
             </v-flex>
           </v-layout>   
           <Footer class="mt-5"></Footer>   
     </v-container>
</template>

<script>
import axios from 'axios';
import Dominio from '@/components/Dominio';
import Subdominios from '@/components/Subdominios';
import Comportamento from '@/components/Comportamento';
import AppHeader from '@/components/header.vue'
import NavDraw from '@/components/navDraw'
import Footer from '@/components/Footer'

export default {
  components: { 
        Dominio, 
        Subdominios,
        Comportamento,
        AppHeader,
        NavDraw,
        Footer
    }, 
  data() {
    return{
      reset_:'',
      formatting: '',
      alignment: '',
      tab: null,
      openHelp: false,
      openImport: false,
      openSubmit: false,
      openConfirmSubmit: false,
      openError: false,
      idImport: '',
      rules: {
          required: [(v) => !!v || "Field is required"],
          repeatedID: [v => this.checkID2(v) || "ID does not exist"],
      },
      items: [
        { tab: 'Caracterizacão'},
        { tab: 'Subdomínios'},
        { tab: 'Comportamento'}
      ],
      domain:{
        _id: '',
        description: 'pt',
        scholarity: '',
        responsible: '',
        notes: '',
        access_type: '',
        body: [],
        default_user_level: '',
        high_performance_factor: '',
        low_performance_factor: '',
        high_skill_factor: '',
        low_skill_factor: '',
        min_questions_number: '',
        question_factor: '',
        inserted_by: "User_default",
        inserted_at:new Date().toLocaleString()
      },
      idDomains: [],
      edit:{
        _id: '',
        description: 'pt',
        scholarity: '',
        responsible: '',
        notes: '',
        access_type: '',
        body: [],
        default_user_level: '',
        high_performance_factor: '',
        low_performance_factor: '',
        high_skill_factor: '',
        low_skill_factor: '',
        min_questions_number: '',
        question_factor: '',
        backlog_factor: '',
        inserted_by: "User_default",
        inserted_at:new Date().toLocaleString()
      }
    }
  },



  methods:{

    handleDataDominios(e) {
      [this.domain._id,this.domain.description,this.domain.scholarity,this.domain.responsible,
      this.domain.notes,this.domain.access_type,this.editing,this.edit._id,this.idDomains] = e;
    },

    handleDataSubdominios(e) {
      this.domain.body = e;
    },

    handleDataComportamento(e) {
      [this.domain.default_user_level,this.domain.high_performance_factor,this.domain.low_performance_factor
      ,this.domain.high_skill_factor,this.domain.low_skill_factor,this.domain.min_questions_number,
      this.domain.question_factor, this.domain.backlog_factor] = e;
    },

    confirmSubmit(){
      if(this.$refs.dm.validate() && this.$refs.sm.validate() && this.$refs.cp.validate()){
        this.openSubmit = true
      }
      else{
        this.openError = true   
      }
    },reset(){
        this.$refs.form.reset()
        this.formData.body.splice(0)
      },

    submit(){
      
      if(this.editing == false){
        let formData = new FormData()
      formData.append('_id', this.domain._id)
      formData.append('description', this.domain.description)
      formData.append('scholarity', this.domain.scholarity)
      formData.append('responsible', this.domain.responsible)
      formData.append('notes', this.domain.notes)
      formData.append('access_type', this.domain.access_type)
      formData.append('body', JSON.stringify(this.domain.body))
      formData.append('default_user_level', this.domain.default_user_level)
      formData.append('high_performance_factor', this.domain.high_performance_factor)
      formData.append('low_performance_factor', this.domain.low_performance_factor)
      formData.append('high_skill_factor', this.domain.high_skill_factor)
      formData.append('low_skill_factor', this.domain.low_skill_factor)
      formData.append('min_questions_number', this.domain.min_questions_number)
      formData.append('backlog_factor', this.domain.backlog_factor)
      formData.append('question_factor', this.domain.question_factor)
      formData.append('inserted_by', this.domain.inserted_by)
      formData.append('inserted_at', this.domain.inserted_at)
        axios.post(`${process.env.VUE_APP_BACKEND}/domain/insert?nome=${this.$store.state.user._id}`, formData,{
          headers: {
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"     
        }
        })
            .then(function(response){
              this.x=response
            },(error) =>{
                console.log(error);
          }); 
      }else{
        let formData = new FormData()
      formData.append('_id', this.domain._id)
      formData.append('description', this.domain.description)
      formData.append('scholarity', this.domain.scholarity)
      formData.append('responsible', this.domain.responsible)
      formData.append('notes', this.domain.notes)
      formData.append('access_type', this.domain.access_type)
      formData.append('body', JSON.stringify(this.domain.body))
      formData.append('default_user_level', this.domain.default_user_level)
      formData.append('high_performance_factor', this.domain.high_performance_factor)
      formData.append('low_performance_factor', this.domain.low_performance_factor)
      formData.append('high_skill_factor', this.domain.high_skill_factor)
      formData.append('low_skill_factor', this.domain.low_skill_factor)
      formData.append('min_questions_number', this.domain.min_questions_number)
      formData.append('question_factor', this.domain.question_factor)
      formData.append('backlog_factor', this.domain.backlog_factor)

      formData.append('inserted_by', this.domain.inserted_by)
      formData.append('inserted_at', this.domain.inserted_at)

        axios.post(`${process.env.VUE_APP_BACKEND}/domain/editar?nome=${this.$store.state.user._id}`, formData,{
          headers: {
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"     
        }
        })
            .then(function(response){
              this.x=response
            },(error) =>{
                console.log(error);
          }); 
      } 
      this.openSubmit = false
      this.openConfirmSubmit = true
    },
    
    reset1 () {
      this.$root.$emit('reset',this.editing)
    },

    startImport() {
      this.openImport = true
    },

    checkID2(item){
      return this.idDomains.find(x => x === item)
    },

    confirmImport(){
      if(this.checkID2(this.idImport)){
        this.$root.$emit('import', this.idImport)
        this.openImport = false
      }
    },

    closeImport() {
      this.openImport = false
    },

    
    closeSubmit() {
      this.openSubmit = false
    },

    closeConfirmSubmit() {
      this.openConfirmSubmit = false
    },

    help() {
      this.openHelp = true
    },

    closeHelp() {
      this.openHelp = false
    },

    closeError() {
      this.openError = false
    }
  }
}
</script>