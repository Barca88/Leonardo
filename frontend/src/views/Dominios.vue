<template>
  <v-container>
    <AppHeader></AppHeader>
    <NavDraw></NavDraw>
    <v-card>
      <v-data-table :headers="headers" 
        :items="navDomains" 
        :items-per-page="15" 
        :search="search" 
        :sort-by="[]"
        multi-sort>
        <template v-slot:top>
          <v-toolbar>
            <v-toolbar-title class>{{ $t('title.domain') }}</v-toolbar-title>
            <v-spacer></v-spacer>

            <v-text-field v-model="search" append-icon="mdi-magnify" :label="$t('title.pesq')" single-line hide-details class="mr-5"></v-text-field>
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">    
                  <v-btn v-bind="attrs" v-on="on" to="/prodDominio" color="#2A3F54" class="white--text mr-4">
                    <v-icon>mdi-text-box-plus-outline</v-icon>
                  </v-btn>                    
                </template>
              <span>{{ $t('opc.cD') }}</span>
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
              <v-icon v-bind="attrs" v-on="on" small class="mr-2" @click="sendItem(item)">mdi-pencil</v-icon>
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
                <h3 width="40" class="white--text"> Domínio - {{this.domain._id}} </h3>
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
                    <dt class="title">Domínio</dt>
                    <dd class="ml-5">{{this.domain.header}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-expansion-panels focusable>
                    <v-expansion-panel
                      v-for="(item,i) in domain.body"
                      :key="i"
                    >
                      <v-expansion-panel-header>Subdomínio {{i+1}}</v-expansion-panel-header>
                      <v-expansion-panel-content>
                          <h4>Subdomínio:</h4> <span>{{item.subdomain}}</span>
                          <h4>Descrição:</h4> <span>{{item.sub_description}}</span>  
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-col>
              </v-row>  
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Descrição</dt>
                    <dd class="ml-5">{{this.domain.description}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Escolaridade</dt>
                    <dd class="ml-5">{{this.domain.scholarity}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                   <dl>
                    <dt class="title">Responsável</dt>
                    <dd class="ml-5">{{this.domain.responsible}}</dd>
                   </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Notas</dt>
                    <dd class="ml-5">{{this.domain.notes}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Tipo de Acesso</dt>
                    <dd class="ml-5">{{this.domain.access_type}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                   <dl>
                    <dt class="title">Nível de Dificuldade</dt>
                    <dd class="ml-5">{{this.domain.default_user_level}}</dd>
                   </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Factor de Desempenho A</dt>
                    <dd class="ml-5">{{this.domain.default_user_level}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Factor de Desempenho B</dt>
                    <dd class="ml-5">{{this.domain.high_performance_factor}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                   <dl>
                    <dt class="title">Factor de Perícia A</dt>
                    <dd class="ml-5">{{this.domain.low_performance_factor}}</dd>
                   </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="4">
                  <dl>
                    <dt class="title">Factor de Perícia B</dt>
                    <dd class="ml-5">{{this.domain.high_skill_factor}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                  <dl>
                    <dt class="title">Número Mínimo de Questões</dt>
                    <dd class="ml-5">{{this.domain.min_questions_number}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="4">
                   <dl>
                    <dt class="title">Factor de Questões</dt>
                    <dd class="ml-5">{{this.domain.question_factor}}</dd>
                   </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <dl>
                    <dt class="title">Data de Criação</dt>
                    <dd class="ml-5">{{this.domain.inserted_at}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="6">
                  <dl>
                    <dt class="title">Inserido Por</dt>
                    <dd class="ml-5">{{this.domain.inserted_by}}</dd>
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
       <!-- Janela para Remoção de Domínio -->
      <v-dialog v-model="dialogDelete" max-width="600px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> REMOVER DOMÍNIO - {{this.domain._id}} </h3>
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
                    <dt class="title">Descrição</dt>
                    <dd class="ml-5">{{this.domain.description}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <dl>
                    <dt class="title">Escolaridade</dt>
                    <dd class="ml-5">{{this.domain.scholarity}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="6">
                  <dl>
                    <dt class="title">Responsável</dt>
                    <dd class="ml-5">{{this.domain.responsible}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <dl>
                    <dt class="title">Tipo de Acesso</dt>
                    <dd class="ml-5">{{this.domain.access_type}}</dd>
                  </dl>
                </v-col>
                 <v-col cols="6">
                  <dl>
                    <dt class="title">Data de Criação</dt>
                    <dd class="ml-5">{{this.domain.inserted_at}}</dd>
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
    <!--v-btn  link to="/prodDominio" color="#2A3F54" class="white--text">
      Novo Domínio
    </v-btn>
    <v-btn link to="/prodQuestao" color="#2A3F54" class="white--text">
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
            itemIndex: -1,
            dialogShow: false,
            dialogDelete: false,
            headers: [
                { text: "Identificador", sortable: true, value: "_id", class: "white--text"},
                { text: "Description",  sortable: true, value: "description", class: "white--text" },
                { text: "Escolaridade",  sortable: true, value: "scholarity", class: "white--text" },
                { text: "Responsável", sortable: true, value: "responsible", class: "white--text"},
                { text: "Data Criação", sortable: true, value: "inserted_at", class: "white--text"},
                { text: "Opções", sortable: false, value: "actions", class: "white--text"},
            ],
            domain: {
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
            search:'',
            navDomains: [],
        }
    },
    created(){
        axios.get(`${process.env.VUE_APP_BACKEND}/domain/getDomains?nome=${this.$store.state.user._id}`,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': "*"    
          }
        })
          .then((response)=>{
            console.log('test ' + response),
            //this.domain = response.data
            this.navDomains=response.data.domains
          },(error) =>{
              console.log(error);
          });
    },
    methods: {
      showItem (item) {
        this.itemIndex = this.navDomains.indexOf(item)
        this.domain = Object.assign({}, item)
        this.dialogShow = true
      },

      sendItem(data){
        this.$router.push({
          name: "ProdDominio", 
          params: { data }
        });
      },

      closeShow(){
        this.dialogShow = false
      },

      deleteItem(item){
        this.itemIndex = this.navDomains.indexOf(item)
        this.domain = Object.assign({}, item)
        this.dialogDelete = true
      },     

      deleteConfirm(){
        axios.delete(`${process.env.VUE_APP_BACKEND}/domain/apagar/` + this.domain._id + `?nome=${this.$store.state.user._id}`,{
          headers: {
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"     
        }
        })
          .then((response)=>{
            console.log(response.data)
            console.log(this.itemIndex)
            this.navDomains.splice(this.itemIndex, 1)
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