<template>
  <v-container>
    <AppHeader></AppHeader>
    <NavDraw></NavDraw>
    <v-card>
      <v-data-table :headers="headers" 
        :items="navQuestoes" 
        :items-per-page="15" 
        :search="search" 
        :sort-by="[]"
        multi-sort>
        <template v-slot:top>
          <v-toolbar>
            <v-toolbar-title class>{{ $t('title.question') }}</v-toolbar-title>
            <v-spacer></v-spacer>

            <v-text-field v-model="search" append-icon="mdi-magnify" :label="$t('title.pesq')" single-line hide-details class="mr-5"></v-text-field>
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">    
                  <v-btn v-bind="attrs" v-on="on" @click="sendItem(null,inf)" color="#2A3F54" class="white--text mr-4">
                    <v-icon>mdi-text-box-plus-outline</v-icon>
                  </v-btn>                    
                </template>
              <span>{{ $t('opc.cQ') }}</span>
            </v-tooltip>
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">    
                  <v-btn v-bind="attrs" v-on="on" color="#2A3F54" class="white--text">
                    <v-icon>mdi-printer</v-icon>
                  </v-btn>                    
                </template>
              <span>Imprimir</span>
            </v-tooltip>
          </v-toolbar>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon v-bind="attrs" v-on="on" small class="mr-2" @click="showItem(item)">mdi-eye</v-icon>
            </template>
            <span>{{ $t('opc.ver') }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon v-bind="attrs" v-on="on" small class="mr-2" @click="sendItem(item,inf)">mdi-pencil</v-icon>
            </template>
            <span>{{ $t('opc.editar') }}</span>
          </v-tooltip>
            
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon v-bind="attrs" v-on="on" small @click="deleteItem(item)">mdi-trash-can</v-icon>
            </template>
            <span>{{ $t('opc.remover') }}</span>
          </v-tooltip>
        </template>
      </v-data-table>
      <!-- Janela para Ver Questão -->
      <v-dialog v-model="dialogShow" max-width="900px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> QUESTÃO - {{this.questao._id}} </h3>
              </div>
            </v-app-bar>
            <v-container>
              <v-row>
                <v-col cols="2">
                  <v-card class="ml-4 mt-1" color="white" flat height="100px" width="110px" >
                      <v-img src="@/assets/questionmark.png"/>
                  </v-card>
                </v-col>
                
                
                <v-col cols="8">
                  <dl>
                    <dt class="title">Pergunta</dt>
                    <dd class="ml-5">{{this.questao.header}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-expansion-panels focusable>
                    <v-expansion-panel
                      v-for="(item,i) in questao.body"
                      :key="i"
                    >
                      <v-expansion-panel-header>Resposta {{i+1}}</v-expansion-panel-header>
                      <v-expansion-panel-content>
                          <h4>Texto da Resposta:</h4> <span>{{item.answer}}</span>
                          <h4>Resposta Correta:</h4> 
                          <span v-if="item.correction == 0">Falso</span><span v-else>Verdadeiro</span>
                          <h4>Resposta Obrigatória:</h4> 
                          <span v-if="item.mandatory == 0">Falso</span><span v-else>Verdadeiro</span>
                          <h4>Resposta Eliminativa:</h4> 
                          <span v-if="item.eliminative == 0">Falso</span><span v-else>Verdadeiro</span>
                          <h4>Pontos:</h4> <span>{{item.points}}</span>

                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-col>
              </v-row>  
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Domínio</dt>
                    <dd class="ml-5">{{this.questao.domain}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Subdomínio</dt>
                    <dd class="ml-5">{{this.questao.subdomain}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Ciclo de Estudos</dt>
                    <dd class="ml-5">{{this.questao.study_cycle}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Escolaridade</dt>
                    <dd class="ml-5">{{this.questao.scholarity}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                   <dl>
                    <dt class="title">Autor</dt>
                    <dd class="ml-5">{{this.questao.author}}</dd>
                   </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Nível de Dificuldade</dt>
                    <dd class="ml-5">{{this.questao.difficulty_level}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Tipo de Questão</dt>
                    <dd class="ml-5">{{this.questao.type_}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                   <dl>
                    <dt class="title">Tempo de Resposta</dt>
                    <dd class="ml-5">{{this.questao.answering_time}}</dd>
                   </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Repetições</dt>
                    <dd class="ml-5">{{this.questao.repetitions}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Modo de Visualização</dt>
                    <dd class="ml-5">{{this.questao.display_mode}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                   <dl>
                    <dt class="title">Idioma</dt>
                    <dd class="ml-5">{{this.questao.language}}</dd>
                   </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Explicação</dt>
                    <dd class="ml-5">{{this.questao.explanation}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Fontes de Informação</dt>
                    <dd class="ml-5">{{this.questao.source}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                   <dl>
                    <dt class="title">Notas</dt>
                    <dd class="ml-5">{{this.questao.notes}}</dd>
                   </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Data de Criação</dt>
                    <dd class="ml-5">{{this.questao.domain}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Inserido Por</dt>
                    <dd class="ml-5">{{this.questao.subdomain}}</dd>
                  </dl>
                </v-col>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Imagem</dt>
                    <v-img v-bind:src="userPic"   />
                  </dl>
                </v-col>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Estado</dt>
                    <dd class="ml-5">{{this.questao.status}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <dl>
                    <dt class="title">Data de Validação</dt>
                    <dd class="ml-5">{{this.questao.validated_at}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="6">
                  <dl>
                    <dt class="title">Validado Por</dt>
                    <dd class="ml-5">{{this.questao.validated_by}}</dd>
                  </dl>
                </v-col>
              </v-row>
            </v-container>
            <v-card-actions>
              <v-container>
                  <v-row >
                    <v-col class="text-right">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">    
                          <v-btn v-bind="attrs" v-on="on" color="#29E898" @click="closeShow" elevation="5" class="mt-5">
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
       <!-- Janela para Remoção de Questão -->
      <v-dialog v-model="dialogDelete" max-width="600px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> REMOVER QUESTÃO - {{this.questao._id}} </h3>
              </div>
            </v-app-bar>
            <v-container>
              <v-row>
                <v-col cols="3">
                  <v-card class="ml-4 mt-1" color="white" flat height="100px" width="110px" >
                      <v-img src="@/assets/delete.png"/>
                  </v-card>
                </v-col>
                <v-col cols="9">
                  <dl>
                    <dt class="title">Pergunta</dt>
                    <dd class="ml-5">{{this.questao.header}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <dl>
                    <dt class="title">Domínio</dt>
                    <dd class="ml-5">{{this.questao.domain}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="6">
                  <dl>
                    <dt class="title">Subdomínio</dt>
                    <dd class="ml-5">{{this.questao.subdomain}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <dl>
                    <dt class="title">Autor</dt>
                    <dd class="ml-5">{{this.questao.author}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="6">
                  <dl>
                    <dt class="title">Data de Criação</dt>
                    <dd class="ml-5">{{this.questao.inserted_at}}</dd>
                  </dl>
                </v-col>
              </v-row>
            </v-container>
            <v-card-actions>
              <v-container>
                  <v-row >
                    <v-col class="text-right">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">    
                          <v-btn v-bind="attrs" v-on="on" color="red" @click="deleteConfirm" elevation="5" class="mt-5 mr-3">
                            <v-icon color="white">mdi-trash-can-outline</v-icon>
                          </v-btn>                    
                        </template>
                      <span>{{ $t('opc.confconfRemov') }}</span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">    
                          <v-btn v-bind="attrs" v-on="on" color="#29E898" @click="closeDelete" elevation="5" class="mt-5">
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
    <!--v-btn to="/prodDominio" color="#2A3F54" class="white--text">
      Novo Domínio
    </v-btn>
    <v-btn to="/prodQuestao" color="#2A3F54" class="white--text">
      Nova Questão
    </v-btn!-->

    <Footer class="mt-5"></Footer>
  </v-container>
</template>

<script>
//imports dos outros componentes e axios para os pedidos
import axios from 'axios'
import AppHeader from '@/components/header.vue'
import NavDraw from '@/components/navDraw'
import Footer from '@/components/Footer'
export default {
    components: { 
        AppHeader,
        NavDraw,
        Footer
    }, 
    data(){
        return{
            cacheKey: 1,
            userPic: '',
            itemIndex: -1,
            dialogShow: false,
            dialogDelete: false,
            headers: [
                { text: "Identificador", sortable: true, value: "_id", class: "white--text"},
                { text: "Domínio",  sortable: true, value: "domain", class: "white--text" },
                { text: "SubDomínio",  sortable: true, value: "subdomain", class: "white--text" },
                { text: "Autor", sortable: true, value: "author", class: "white--text"},
                { text: "Data Criação", sortable: true, value: "inserted_at", class: "white--text"},
                { text: "Opções", sortable: false, value: "actions", class: "white--text"},
            ],
            inf : "/questions",
            questao:{
              _id: '',
              language: '',
              study_cycle: '',
              scholarity: '',
              domain: '',
              subdomain: '',
              difficulty_level: '',
              author: '',
              display_mode: '',
              answering_time: '',
              type: '',
              precedence: [],
              repetitions: '',
              header:'',
              body: [],
              explanation: '',
              images: '',
              videos: '',
              source: '',
              notes: '',
              status: '',
              inserted_by: '',
              inserted_at: '',
              validated_by: '',
              validated_at: ''
            },
            search:'',
            navQuestoes: [],
            dominios: []
        }
    },
    created(){
      Object.assign(this.$data, this.$options.data())
      this.userPic=''
        axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions?nome=${this.$store.state.user._id}&flag=aproved`,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': "*"    
          }
        })
          .then((response)=>{
            console.log(response.data)
            //this.domain = response.data
            this.navQuestoes=response.data.questions
            this.dominios=response.data.domains
            
          },(error) =>{
              console.log(error);
          });
    },
    methods: {
      showItem (item) {
        this.itemIndex = this.navQuestoes.indexOf(item)
        this.questao = Object.assign({}, item)
        this.showImage(this.questao._id)
        this.dialogShow = true
      },
      showImage(_qId){

        this.userPic=''
        axios.get(`${process.env.VUE_APP_BACKEND}/question/foto/` + _qId,  {
            responseType:'arraybuffer',
            headers: {
                'Authorization': `Bearer: ${this.$store.state.jwt}`
            }
        })
        .then(response => {
            var image = new Buffer(response.data, 'binary').toString('base64')
            this.userPic = `data:${response.headers['content-type'].toLowerCase()};base64,${image}`
        }).catch(e => {
            console.log('Erro ' + e)
            this.errors.push(e)
        })

      },

      sendItem(data,inf){
        this.$router.push({
          name: "ProdQuestao", 
          params: { data, inf }
        });
      },

      closeShow(){
        this.dialogShow = false
      },

      deleteItem(item){
        this.itemIndex = this.navQuestoes.indexOf(item)
        this.question = Object.assign({}, item)
        this.dialogDelete = true
      },     

      deleteConfirm(){
        axios.delete(`${process.env.VUE_APP_BACKEND}/question/delete/` + this.question._id + `?nome=${this.$store.state.user._id}`,{
          headers: {
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"     
        }
        })
          .then((response)=>{
            this.x=response
            this.navQuestoes.splice(this.itemIndex, 1)
          },(error) =>{
              console.log(error);
          });
        this.closeDelete()
      },

      closeDelete(){
        this.dialogDelete = false
      }
    },

}
</script>
<style scoped>
    /* css para tornar a aparência mais similar ao template */
    .v-data-table /deep/ th{
        background-color:#4b779e;
        ;
    }
    .v-data-table /deep/ tr{
        color: #73879C;
        font-size: 13px;
    }
    .v-data-table /deep/ tr:nth-child(even){
        background-color: rgb(245, 245, 245);
    }

    a { 
      text-decoration: none; 
    }

    .title {
      color: #2A3F54
    }


</style>