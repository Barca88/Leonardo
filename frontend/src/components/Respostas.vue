<template>
  <v-container>
    <v-form v-model="valid" ref="form">
      <v-card elevation="3">
        <h2 class="titulo mb-4 ml-3">Questão {{this.idQuestao}}</h2>
        <p class="field ml-5">Domínio: <span class="fieldtext">{{this.domain}}</span></p>
        <p class="field ml-5">Pergunta: <span class="fieldtext">{{this.header}}</span></p>
        <v-divider></v-divider>
      </v-card>
      <v-row>
        <v-col cols="8">
          <div v-if="firstResposta">
            <v-text-field class="mt-4" v-model="resposta.answer" :rules="[...rules.repeatedID]" :counter="200" label="Texto da Resposta"></v-text-field>
          </div>
          <div v-else>
            <v-text-field class="mt-4" v-model="resposta.answer" :rules="[...rules.required,...rules.repeatedID]" :counter="200" label="Texto da Resposta"></v-text-field>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="6" xl="2" lg="3" md="3" sm="6" class="mt-4">
          <p class="grey--text text--darken-1">Resposta Correta:</p>
        </v-col>
        <v-col cols="6" lg="3" md="3" sm="6">
          <v-radio-group v-model="resposta.correction" row mandatory>
            <v-radio label="0" value="0"></v-radio>

            <v-radio label="1" value="1"></v-radio>

          </v-radio-group>
        </v-col>
        <v-col xl="2" lg="3" md="3" sm="6" class="mt-4">
          <p class="grey--text text--darken-1">Resposta Obrigatória:</p>
        </v-col>
        <v-col lg="3" md="3" sm="6">
          <v-radio-group v-model="resposta.mandatory" row mandatory>

            <v-radio label="0" value="0"></v-radio>

            <v-radio label="1" value="1"></v-radio>

          </v-radio-group>
        </v-col>
      </v-row>

      <v-row>
        <v-col xl="2" lg="3" md="3" sm="4" class="mt-4">
          <p class="grey--text text--darken-1">Resposta Eliminatória:</p>
        </v-col>
        <v-col lg="3" md="3" sm="6">
          <v-radio-group v-model="resposta.eliminative" row mandatory>

            <v-radio label="0" value="0"></v-radio>

            <v-radio label="1" value="1"></v-radio>
          </v-radio-group>
        </v-col>
        <v-col cols="6">
          <v-select :items="pontos" v-model="resposta.points" label="Pontos" dense></v-select>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" align="right" class="mb-5">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">    
              <v-btn v-bind="attrs" v-on="on" @click="addAnswer" class="mr-5" color="#2A3F54">
                 <v-icon color="white">mdi-plus</v-icon>
              </v-btn>                    
            </template>
            <span>Adicionar Resposta</span>
          </v-tooltip>
        </v-col>
      </v-row>

      <v-card class="mx-auto" tile>
        <v-card-title>Respostas</v-card-title>

        <v-data-table :headers="headers" :items="formData.body" disable-pagination :hide-default-footer="true" fixed-header class="mb-5">
          <template v-slot:[`item.index`]="props">{{ props.index+1 }}</template>
          <template v-slot:[`item.answer`]="{ item }">
            {{ item.answer.length > 10 ? item.answer.slice(0, 10) + '...' : item.answer }}
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-icon v-bind="attrs" v-on="on" small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
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

        <!--Janela para Edição de Resposta -->
        <v-dialog v-model="dialogEdit" max-width="700px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> Editar Resposta</h3>
              </div>
            </v-app-bar>
            <v-container>
              <v-row>
                <v-col cols="8">
                  <v-text-field v-model="respostaEdit.answer" 
                    class="mt-4"
                    :rules="rules.required" 
                    :counter="200" 
                    label="Texto da Resposta"
                 ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="6" xl="2" lg="3" md="3" sm="6" class="mt-4">
                  <p class="grey--text text--darken-1">Resposta Correta:</p>
                </v-col>
                <v-col cols="6" lg="3" md="3" sm="6">
                  <v-radio-group v-model="respostaEdit.correction" row mandatory>
                    <v-radio label="0" value="0"></v-radio>

                    <v-radio label="1" value="1"></v-radio>

                  </v-radio-group>
                </v-col>
                <v-col xl="2" lg="3" md="3" sm="6" class="mt-4">
                  <p class="grey--text text--darken-1">Resposta Obrigatória:</p>
                </v-col>
                <v-col lg="3" md="3" sm="6">
                  <v-radio-group v-model="respostaEdit.mandatory" row mandatory>

                    <v-radio label="0" value="0"></v-radio>

                    <v-radio label="1" value="1"></v-radio>

                  </v-radio-group>
                </v-col>
              </v-row>

              <v-row>
                <v-col xl="2" lg="3" md="3" sm="4" class="mt-4">
                  <p class="grey--text text--darken-1">Resposta Eliminatória:</p>
                </v-col>
                <v-col lg="3" md="3" sm="6">
                  <v-radio-group v-model="respostaEdit.eliminative" row mandatory>

                    <v-radio label="0" value="0"></v-radio>

                    <v-radio label="1" value="1"></v-radio>
                  </v-radio-group>
                </v-col>
                <v-col cols="6">
                  <v-select :items="pontos" v-model="respostaEdit.points" label="Pontos" dense></v-select>
                </v-col>
              </v-row>
            </v-container>
            <v-card-actions>
              <v-container>
                  <v-row >
                    <v-col class="text-right">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="#F0B62B" @click="editConfirm" v-bind="attrs" v-on="on" elevation="5" class=" mr-3">
                            <v-icon color="white">mdi-checkbox-marked-outline</v-icon>
                          </v-btn>
                        </template>
                        <span>{{ $t('opc.confEdit') }}</span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="#29E898" @click="closeEdit" v-bind="attrs" v-on="on" elevation="5">
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

        <!--Janela de Aviso na Inserção de Reposta -->
        <v-dialog v-model="dialogResp" max-width="400px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> Aviso </h3>
              </div>
            </v-app-bar>
            <v-container>
              <v-row>
                
                <v-col cols="12">
                  <h3 class="ml-5 mt-5">Para adicionar uma nova resposta, todos os campos têm que estar preenchidos!</h3>
                </v-col>
              </v-row>
            </v-container>
            <v-card-actions>
              <v-container>
                <v-row >
                    <v-col class="text-right">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="#29E898" @click="closeResp" v-bind="attrs" v-on="on" elevation="5">
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

        <!--Janela para Remoção de Resposta -->
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> Remover Resposta </h3>
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
                  <h3 class="ml-5 mt-5">Tem a certeza que pretende remover a Resposta?</h3>
                </v-col>
              </v-row>
            </v-container>
            <v-card-actions>
              <v-container>
                <v-row >
                    <v-col class="text-right">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="#F0B62B" @click="deleteConfirm" v-bind="attrs" v-on="on" elevation="5" class=" mr-3">
                            <v-icon color="white">mdi-checkbox-marked-outline</v-icon>
                          </v-btn>
                        </template>
                        <span>{{ $t('opc.confconfRemov') }}</span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="#29E898" @click="closeDelete" v-bind="attrs" v-on="on" elevation="5">
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
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            valid:'',
            idQuestao: '',
            domain: '',
            header: '',
            editedIndex: -1,
            firstResposta: false,
            editing: false,
            dialogEdit: false,
            dialogResp: false,
            dialogDelete: false,
            pontos: ['1', '2', '3'],
            formData: {
                body: []
            },
            resposta: {
                answer: "",
                correction: "",
                mandatory: "",
                eliminative: "",
                points: ""
            },
            respostaEdit: {
                answer: "",
                correction: "",
                mandatory: "",
                eliminative: "",
                points: ""
            },
            defaultResp: {
                answer: "",
                correction: "",
                mandatory: "",
                eliminative: "",
                points: ""
            },
            rules: {
                repeatedID: [v => this.checkID(v) || "ID already exists"],
                required: [(v) => !!v || "Field is required"],
                length30: [v => (v && v.length <= 30) || "Field must be less or equal than 30 characters"],
                length75: [v => (v && v.length <= 75) || "Field must be less or equal than 75 characters"],
                length100: [v => (v && v.length <= 100) || "Field must be less or equal than 100 characters"],
            },
            headers: [
                { text: "Número", align: "start", sortable: false, value: "index" },
                { text: "Texto",  sortable: false, value: "answer" },
                { text: "Correta",  sortable: false, value: "correction" },
                { text: "Obrigatória", sortable: false, value: "mandatory" },
                { text: "Eliminatória", sortable: false, value: "eliminative" },
                { text: "Pontos", sortable: false, value: "points" },
                { text: "Actions", sortable: false, value: "actions"},
            ],
        }
    },
    created() {
      if(this.$route.params.data!=null){
        this.firstResposta = true
        let data = this.$route.params.data
            this.formData.body = data.body         
      }  
    },

    mounted() {
      this.$root.$on('change', data => {
            this.idQuestao = data.sendId
            this.domain = data.sendDomain
            this.header = data.sendHeader
      })
      this.$root.$on('import', data => {
            axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions/`+ data)
              .then((response)=>{
                this.firstResposta = true
                this.formData.body = response.data.question.body
              },(error) =>{
                  console.log(error);
              });
      })
      this.$root.$on('reset', data => {
        console.log(data)
        this.formData.body = []
        this.resposta.answer = ""
        this.resposta.correction = ""
        this.resposta.mandatory = ""
        this.resposta.eliminative = ""
        this.resposta.points = ""
      })
    },

    methods: {

      validate() {
        return this.$refs.form.validate() //&& this.formData.body.length!=0
      },

      addAnswer(){
        if(this.resposta.answer != "" && this.resposta.points != ""){
          if(this.checkID(this.resposta.answer)){
            this.formData.body.push(this.resposta);
            this.resposta = Object.assign({}, this.defaultResp)
            if(!this.firstResposta){
              this.firstResposta = true
            }
          }else{
            this.dialogResp = true
          }
        }else{
          this.dialogResp = true
        }
      },

       editItem (item) {
        this.editedIndex = this.formData.body.indexOf(item)
        this.respostaEdit = Object.assign({}, item)
        this.dialogEdit = true
      },

      editConfirm() {
        if(!this.respostaEdit.points){
          this.dialogResp = true
        }
        else{
          this.firstResposta = true
          this.$set(this.formData.body, this.editedIndex, this.respostaEdit)
          this.resposta = Object.assign({}, this.defaultResp)
          this.dialogEdit = false
        }
      },

      deleteItem (item) {
        this.editedIndex = this.formData.body.indexOf(item)
        this.dialogDelete = true
      },     

      deleteConfirm () {
        if(this.editedIndex == 0){
          this.formData.body.splice(this.editedIndex, 1)
          this.firstResposta = false
          this.closeDelete()
        }else{
          this.formData.body.splice(this.editedIndex, 1)
          this.closeDelete()
        }
      },

      closeEdit(){
        this.resposta = Object.assign({}, this.defaultSub)
        this.dialogEdit = false
        this.editedIndex = -1
      },

      closeResp(){
        this.dialogResp = false
      },

      checkID(item){
        return !this.formData.body.find(x => x.answer === item)
      },

      closeDelete(){
        this.dialogDelete = false
        this.editedIndex = -1
      },
    },

    watch: {
        formData: {
            handler: function() {
              this.$emit('newdataRespostas', this.formData.body);
          },
            deep: true
        },
      },
}
</script>

<style scoped>
  h2.titulo{
    color:#2A3F54;
  }
  p.field{
    color:#2A3F54;
  }
  span.fieldtext{
    color:black;
  }
</style>