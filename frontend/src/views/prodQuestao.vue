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
                      <v-card-title class="yellow--text text--darken-2 text-h4 mr-5">Produção</v-card-title>
                      <v-card-subtitle class="white--text text-h5">Preparação de Questões</v-card-subtitle>
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
                      <Caracterizacao ref="ct" @newdataCaracterizacao="handleDataCaracterizacao($event)"/>
                   </v-tab-item>
                   <v-tab-item eager>
                      <Respostas ref="rp" @newdataRespostas="handleDataRespostas($event)"/>
                   </v-tab-item>
                   <v-tab-item eager>
                      <Suporte ref="sp" @newdataSuporte="handleDataSuporte($event)"/>
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
                      <span>Submit</span>
                    </v-tooltip>

                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">    
                        <v-btn v-bind="attrs" v-on="on" color="white" elevation="5" class="mr-2" @click="startImport">
                          <v-icon color="black">mdi-import</v-icon>
                        </v-btn>                    
                      </template>
                      <span>Import</span>
                    </v-tooltip>

                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">    
                        <v-btn v-bind="attrs" v-on="on" color="#29E898" elevation="5" @click="reset1">
                          <v-icon color="white">mdi-broom</v-icon>
                        </v-btn>                    
                      </template>
                      <span>Reset</span>
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
                      <span>Help</span>
                    </v-tooltip>

                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">    
                         <v-btn v-bind="attrs" v-on="on" to="/questions" color="#29E898" elevation="5" class="">
                          <v-icon color="white">mdi-door-open</v-icon>
                        </v-btn>                    
                      </template>
                      <span>Sair</span>
                    </v-tooltip>
                  </v-btn-toggle>
                </v-row>
                <!-- Janela para Confirmação da Submissão -->
                <v-dialog v-model="openSubmit" max-width="500px">
                  <v-card>
                    <v-app-bar color="#2A3F54" >
                      <div class="d-flex align-center">
                        <h3 width="40" class="white--text"> Confirmar Submissão</h3>
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
                          <h3 class="ml-5 mt-5">Pretende confirmar a submissão da questão?</h3>
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
                                <span>Submit</span>
                              </v-tooltip>

                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#29E898" @click="closeSubmit" elevation="5" class="mt-5">
                                    <v-icon color="white">mdi-door-open</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>Sair</span>
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
                        <h3 width="40" class="white--text"> Submissão de Questão</h3>
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
                          <h3 class="ml-5 mt-5">Submissão de Questão com Sucesso!</h3>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-card-actions>
                      <v-container>
                          <v-row >
                            <v-col class="text-right">
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#29E898" to="/questions" @click="closeConfirmSubmit" elevation="5" class="mt-5">
                                    <v-icon color="white">mdi-door-open</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>Sair</span>
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
                        <h3 width="40" class="white--text"> Erro na Submissão</h3>
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
                          <h3 class="ml-5 mt-5">Erro na submissão da questão!</h3>
                          <h3 class="ml-5">Por favor preencha todos os campos obrigatórios.</h3>
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
                                <span>Sair</span>
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
                        <h3 width="40" class="white--text"> Import de Questão</h3>
                      </div>
                    </v-app-bar>
                    <v-container>
                      <v-row>
                        <v-col cols="9">
                          <h3 class="ml-5 mt-5">Insira o identificador da questão que pretende importar.</h3>
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
                                <span>Import</span>
                              </v-tooltip>
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">   
                                  <v-btn v-bind="attrs" v-on="on" color="#29E898" @click="closeImport" elevation="5" class="mt-5">
                                    <v-icon color="white">mdi-door-open</v-icon>
                                  </v-btn>                     
                                </template>
                                <span>Sair</span>
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
                        <h3 width="40" class="white--text"> Ajuda</h3>
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
                          <h3 class="ml-5 mt-5">Preencha todos os campos que constituem a questão.</h3>
                          <h3 class="ml-5">Navegue por todas as tabs para garantir que toda a informação se encontra correta.</h3>
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
                                <span>Sair</span>
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
import Caracterizacao from '@/components/Caracterizacao'
import Respostas from '@/components/Respostas'
import Suporte from '@/components/Suporte'
import AppHeader from '@/components/header.vue'
import NavDraw from '@/components/navDraw'
import Footer from '@/components/Footer'

export default {
  components: { 
        Caracterizacao, 
        Respostas,
        Suporte,
        AppHeader,
        NavDraw,
        Footer
    }, 
  data() {
    return{
      reset:'',
      formatting: '',
      alignment: '',
      tab: null,
      openHelp: false,
      openImport: false,
      openSubmit: false,
      openConfirmSubmit: false,
      openError: false,
      idImport: '',
      editing: false,
      rules: {
          required: [(v) => !!v || "Field is required"],
          repeatedID: [v => this.checkID2(v) || "ID does not exist"],
      },
      items: [
        { tab: 'Caracterizacão'},
        { tab: 'Respostas'},
        { tab: 'Suporte'}
      ],
      questao:{
        id: '',
        language: "pt", 
        study_cycle: '',
        scholarity: '',
        domain: '',
        subdomain: '',
        subsubdomain: '',
        difficulty_level: '',
        author: '',
        display_mode: '', 
        answering_time: '',
        type: '',
        precedence: [], 
        repetitions: '',
        header:'',
        body: [], 
        explanation: "", 
        images: {}, 
        videos: "", 
        source: "", 
        notes: "", 
        status:"E", 
        inserted_by: "User_default", 
        inserted_at:new Date().toLocaleString(), 
        validated_by:"", 
        validated_at:"" 
      },
      idQuestion: [],
      edit:{
        _id: null,
        id: '',
        language: "pt", 
        study_cycle: '',
        scholarity: '',
        domain: '',
        subdomain: '',
        subsubdomain: '',
        difficulty_level: '',
        author: '',
        display_mode: '', 
        answering_time: '',
        type: '',
        precedence: [], 
        repetitions: '',
        header:'',
        body: [], 
        explanation: "", 
        images: {}, 
        videos: "", 
        source: "", 
        notes: "", 
        status:"E", 
        inserted_by: "User_default", 
        inserted_at:new Date().toLocaleString(), 
        validated_by:"", 
        validated_at:"" 
      },
    }
  },
 
  created() {
      axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions`,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"   
          }
        })
      .then((response)=>{
        response.data.questions.forEach((obj) =>{
          this.idQuestion.push(obj._id)
        });
      },(error) =>{
          console.log(error);
    });

    },


  methods:{

    handleDataCaracterizacao(e) {
      [this.questao._id,this.questao.study_cycle,this.questao.scholarity,this.questao.domain,this.questao.subdomain,
      this.questao.subsubdomain, this.questao.header, this.questao.difficulty_level,this.questao.author,this.questao.display_mode,
      this.questao.answering_time,this.questao.type_,this.questao.precedence,this.questao.repetitions,this.editing,this.edit._id] = e;
    },

    handleDataRespostas(e) {
      this.questao.body = e;
    },

    handleDataSuporte(e) {
      [this.questao.images, this.questao.explanation,this.questao.notes,this.questao.source,this.questao.status,this.questao.language] = e;
    },

    confirmSubmit(){
      if(this.$refs.ct.validate() && this.$refs.rp.validate() && this.$refs.sp.validate()){
        this.openSubmit = true
      }
      else{
        this.openError = true   
      } 
    },

    submit(){
      console.log('Submit')
      if(this.editing == false){
        console.log('A enviar')
        let formData = new FormData()
        formData.append('_id', this.questao._id)
        formData.append('language' , this.questao.language)
        formData.append('study_cycle' , this.questao.study_cycle)
        formData.append('scholarity' , this.questao.scholarity)
        formData.append('domain' , this.questao.domain)
        formData.append('subdomain' , this.questao.subdomain)
        formData.append('subsubdomain' , this.questao.subsubdomain)
        formData.append('difficulty_level' , this.questao.difficulty_level)
        formData.append('author' , this.questao.author)
        formData.append('display_mode' , this.questao.display_mode)
        formData.append('answering_time' , this.questao.answering_time)
        formData.append('type' , this.questao.type_)
        formData.append('precedence' , this.questao.precedence)
        formData.append('repetitions' , this.questao.repetitions)
        formData.append('header' , this.questao.header)
        formData.append('body' , JSON.stringify(this.questao.body))
        formData.append('explanation' , this.questao.explanation)
        formData.append('images' , this.questao.images)
        formData.append('videos' , this.questao.videos)
        formData.append('source' , this.questao.source)
        formData.append('notes' , this.questao.notes)
        formData.append('status' , this.questao.status)
        formData.append('inserted_by' , this.questao.inserted_by)
        formData.append('inserted_at' , this.questao.inserted_at)
        formData.append('validated_by' , this.questao.validated_by)
        formData.append('validated_at' , this.questao.validated_at)
        axios.post(`${process.env.VUE_APP_BACKEND}/question/insert?nome=${this.$store.state.user._id}`, formData,{
            headers: {
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"     
        }
        })
            .then(function(response){
              console.log(response)
            },(error) =>{
                console.log(error);
          }); 

          console.log('Enviado')
      }else{
        console.log('A Editar')
        let formData = new FormData()
        formData.append('_id', this.questao._id)
        formData.append('language' , this.questao.language)
        formData.append('study_cycle' , this.questao.study_cycle)
        formData.append('scholarity' , this.questao.scholarity)
        formData.append('domain' , this.questao.domain)
        formData.append('subdomain' , this.questao.subdomain)
        formData.append('subsubdomain' , this.questao.subsubdomain)
        formData.append('difficulty_level' , this.questao.difficulty_level)
        formData.append('author' , this.questao.author)
        formData.append('display_mode' , this.questao.display_mode)
        formData.append('answering_time' , this.questao.answering_time)
        formData.append('type' , this.questao.type_)
        formData.append('precedence' , this.questao.precedence)
        formData.append('repetitions' , this.questao.repetitions)
        formData.append('header' , this.questao.header)
        formData.append('body' , JSON.stringify(this.questao.body))
        formData.append('explanation' , this.questao.explanation)
        formData.append('images' , this.questao.images)
        formData.append('videos' , this.questao.videos)
        formData.append('source' , this.questao.source)
        formData.append('notes' , this.questao.notes)
        formData.append('status' , this.questao.status)
        formData.append('inserted_by' , this.questao.inserted_by)
        formData.append('inserted_at' , this.questao.inserted_at)
        formData.append('validated_by' , this.questao.validated_by)
        formData.append('validated_at' , this.questao.validated_at)
      
        axios.post(`${process.env.VUE_APP_BACKEND}/question/edit?nome=${this.$store.state.user._id}`, formData,{
            headers: {
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"     
        }
        })
            .then(function(response){
              console.log(response)
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

    checkID2(item){
      return this.idQuestion.find(x => x === item)
    },

    confirmImport(){
      if(this.checkID2(this.idImport)){
        console.log("Import : " + this.idImport)
        this.$root.$emit('import', this.idImport)
        this.openImport = false
      }
    },

    startImport() {
      this.openImport = true
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
    },
  }
}
</script>



