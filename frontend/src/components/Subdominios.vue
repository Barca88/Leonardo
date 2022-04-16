<template>
  <v-container>
    <v-form v-model="valid" ref="form">
      <v-card elevation="3">
        <h2 class="titulo mb-4 ml-3">Domínio {{this.idDominio}}</h2>
        <p class="field ml-5">Descrição: <span class="fieldtext">{{this.description}}</span></p>
        <v-divider></v-divider>
      </v-card>

      <v-row>
        <v-col cols="8">
          <div v-if="firstSub">
            <v-text-field class="mt-4" v-model="subdominio.subdomain" :rules="[...rules.repeatedID]" :counter="200" label="Subdomínio"></v-text-field>
          </div>
          <div v-else>
            <v-text-field class="mt-4" v-model="subdominio.subdomain" :rules="[...rules.required,...rules.repeatedID]"  :counter="200" label="Subdomínio"></v-text-field>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="8">
          <div v-if="firstSub">
            <v-textarea v-model="subdominio.sub_description" label="Descrição" counter outlined auto-grow background-color="#f2f2fc" color="#2A3F54" rows="3" placeholder="Introduza uma Descrição para o Subdomínio"></v-textarea>
          </div>
          <div v-else>
            <v-textarea v-model="subdominio.sub_description" label="Descrição" counter outlined auto-grow background-color="#f2f2fc" color="#2A3F54" rows="3" :rules="rules.required" placeholder="Introduza uma Descrição para o Subdomínio"></v-textarea>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" align="right" class="mb-5">
          <v-btn @click="addSubdominio" class="mr-5" color="#2A3F54">
            <v-icon color="white">mdi-plus</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-card class="mx-auto" tile>
        <v-card-title>Lista de Subdomínios</v-card-title>

        <v-data-table :headers="headers" :items="formData.body" disable-pagination :hide-default-footer="true" fixed-header class="mb-5">

          <template v-slot:[`item.index`]="props">
            {{ props.index+1 }}
          </template>

          <template v-slot:[`item.subdomain`]="{ item }">
            {{item.subdomain != null && item.subdomain.length > 15 ? item.subdomain.slice(0, 15) + '...' : item.subdomain }}
          </template>

          <template v-slot:[`item.sub_description`]="{ item }">
            {{item.sub_description != null && item.sub_description.length > 15 ? item.sub_description.slice(0, 15) + '...' : item.sub_description }}
          </template>

          <template v-slot:[`item.actions`]="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-icon v-bind="attrs" v-on="on" small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
              </template>
              <span>Editar</span>
            </v-tooltip>
            
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-icon v-bind="attrs" v-on="on" small @click="deleteItem(item)">mdi-delete</v-icon>
              </template>
              <span>Remover</span>
            </v-tooltip>
          </template>
        </v-data-table>



        <!--Janela para Edição de Subdomínio -->
        <v-dialog v-model="dialogEdit" max-width="700px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> Editar Subdomínio</h3>
              </div>
            </v-app-bar>
            <v-container>
              <v-row>
                <v-col cols="8">
                  <v-text-field v-model="subdominioEdit.subdomain" :rules="rules.required" :counter="200" label="Subdomínio" disabled></v-text-field>
                </v-col>
              </v-row>

              <v-row class="mt-5">
                <v-col cols="12" md="12">
                  <v-textarea v-model="subdominioEdit.sub_description" label="Descrição" counter outlined auto-grow background-color="#f2f2fc" color="#2A3F54" rows="3" :rules="rules.required" placeholder="Introduza uma Descrição para o Subdomínio"></v-textarea>
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
                        <span>Confirmar Edição</span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="#29E898" @click="closeEdit" v-bind="attrs" v-on="on" elevation="5">
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

        <!--Janela de Aviso na Inserção de Subdominio -->
        <v-dialog v-model="dialogSub" max-width="400px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> Aviso </h3>
              </div>
            </v-app-bar>
            <v-container>
              <v-row>
                
                <v-col cols="12">
                  <h3 class="ml-5 mt-5">Para adicionar um novo Subdomínio, todos os campos têm que estar preenchidos!</h3>
                </v-col>
              </v-row>
            </v-container>
            <v-card-actions>
              <v-container>
                <v-row >
                    <v-col class="text-right">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="#29E898" @click="closeSub" v-bind="attrs" v-on="on" elevation="5">
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

        <!--Janela para Remoção de Subdomínio -->
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> Remover Subdomínio </h3>
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
                  <h3 class="ml-5 mt-5">Tem a certeza que pretende remover o Subdomínio?</h3>
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
                        <span>Confirmar Remoção</span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="#29E898" @click="closeDelete" v-bind="attrs" v-on="on" elevation="5">
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
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            valid:'',
            idDominio: '',
            description: '',
            editedIndex: -1,
            firstSub: false,
            editing: false,
            dialogEdit: false,
            dialogSub: false,
            dialogDelete: false,
            formData: {
                body: [],
            },
            subdominio: {
                designation: "",
                description: ""
            },
            subdominioEdit: {
                designation: "",
                description: ""
            },
            defaultSub: {
                designation: "",
                description: ""
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
                { text: "Subdomínio",  sortable: false, value: "subdomain" },
                { text: "Descrição",  sortable: false, value: "sub_description" },
                { text: "Actions", sortable: false, value: "actions"},
            ],
        }
    },
  
    created() {
      if(this.$route.params.data!=null){
        this.firstSub = true
        let data = this.$route.params.data
            this.formData.body = data.body         
      }  
    },

    mounted() {
      this.$root.$on('change', data => {
            //console.log("change2 : " + data.sendDescription)
            this.idDominio = data.sendId
            this.description = data.sendDescription
      })
      this.$root.$on('import', data => {
            axios.get(`${process.env.VUE_APP_BACKEND}/domain/getDomains/`+ data)
              .then((response)=>{
                this.firstSub = true
                this.formData.body = response.data.domain.body
                this.editing = true
              },(error) =>{
                  console.log(error);
              });
      })
      this.$root.$on('reset', data => {
        console.log(data)
        this.formData.body = []
        this.subdominio.subdomain = ""
        this.subdominio.sub_description = ""
      })
    },

    methods: {

      validate(){
        console.log('Validating')
        return this.$refs.form.validate()
      },

      addSubdominio(){
        if(this.subdominio.subdomain != undefined && this.subdominio.sub_description != undefined){
          if(this.checkID(this.subdominio.subdomain)){
            this.formData.body.push(this.subdominio);
            this.subdominio = Object.assign({}, this.defaultSub)
            //console.log("formADD : " + this.formData.body[0].subdomain)
          }
          else{
            this.dialogSub = true
          }
          if(!this.firstSub){
            this.firstSub = true
          }
        }else{
          this.dialogSub = true
        }
      },

      editItem(item){
        this.editedIndex = this.formData.body.indexOf(item)
        this.subdominioEdit = Object.assign({}, item)
        this.dialogEdit = true
      },


    checkID(item){
      return !this.formData.body.find(x => x.subdomain === item)
    },


      editConfirm(){
        if(!this.subdominioEdit.sub_description){
          this.dialogSub = true
        }
        else{
          this.firstSub = true
          this.$set(this.formData.body, this.editedIndex, this.subdominioEdit) 
          //this.formData.body = this.subdominioEdit
          this.subdominio = Object.assign({}, this.defaultSub)
          this.dialogEdit = false
        }
      },

      closeEdit(){
        this.subdominioEdit = Object.assign({}, this.defaultSub)
        this.dialogEdit = false
        this.editedIndex = -1
      },

      deleteItem(item){
        this.editedIndex = this.formData.body.indexOf(item)
        this.dialogDelete = true
      },    
      
      deleteConfirm(){
        if(this.editedIndex == 0){
          this.formData.body.splice(this.editedIndex, 1)
          this.firstSub = false
          this.closeDelete()
        }else{
          this.formData.body.splice(this.editedIndex, 1)
          this.closeDelete()
        }
      },

      closeDelete(){
        this.dialogDelete = false
        this.editedIndex = -1
      },

      closeSub () {
        this.dialogSub = false
      },
    },
    watch: {
        formData: {
            handler: function() {
              //console.log("form : " + this.formData.body[0].subdomain)
              this.$emit('newdataSubdominio', this.formData.body);
            },
            deep: true
        }
      }
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
