<template>
    <div id="users">
        <appHeader :ajuda='ajuda'></appHeader>
        <navDraw></navDraw>
        <v-data-table
            :headers="headers"
            :items="users"
            :items-per-page="15"
            :sort-by="['_id']"
            :search="search"
            multi-sort       
        ><template v-slot:top>
            <v-toolbar flat color="white">
                <v-toolbar-title>{{$t('users.titleRes')}}</v-toolbar-title>
                <v-divider
                class="mx-4"
                inset
                vertical
                ></v-divider>
                <v-spacer></v-spacer>
                <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  :label="`${$t('navd.se')}`"
                  single-line
                  hide-details
                  class="mr-5"
                ></v-text-field>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">    
                        <v-btn v-bind="attrs" v-on="on" @click="editItem({}, 'adicionar')" color="#2A3F54" class="white--text mr-4">
                            <v-icon>mdi-account-plus</v-icon>
                        </v-btn>                    
                        </template>
                    <span>{{ $t('opc.cU') }}</span>
                    </v-tooltip>
            </v-toolbar>
        </template>
        <template v-slot:header._id="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.name="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.email="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.type="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.options="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:item.options="{ item }">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-icon
                        v-bind="attrs" v-on="on"
                        small
                        color="#246a73"
                        class="mr-2"
                        @click="editItem(item, 'ver')"
                    >
                    mdi-eye
                    </v-icon>
                </template>
                <span>{{ $t('opc.ver') }}</span>
            </v-tooltip>
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-icon
                        v-bind="attrs" v-on="on"
                        small
                        color="#368f8b"
                        class="mr-2"
                        @click="editItem(item,'editar')"
                    >
                        mdi-pencil
                    </v-icon>
                </template>
                <span>{{ $t('opc.editar') }}</span>
            </v-tooltip>
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-icon
                        v-bind="attrs" v-on="on"
                        small
                        color="#246a73"
                        class="mr-2"
                        @click="verObjectItem(item,'curriculo')"
                    >
                        mdi-text-box-multiple
                    </v-icon>
                </template>
                <span>{{ $t('opc.currículo') }}</span>
            </v-tooltip>
             <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-icon
                        v-bind="attrs" v-on="on"
                        small
                        color="#55bcc9"
                        class="mr-2"
                        @click="verObjectItem(item,'foto')"
                    >
                        mdi-camera
                    </v-icon>
                </template>
                <span>{{ $t('opc.foto') }}</span>
            </v-tooltip>

            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-icon
                        v-bind="attrs" v-on="on"
                        small
                        color="#8e363a"
                        class="mr-2"
                        @click="deleteDialog = true;tempValue=item"
                    >
                        mdi-trash-can
                    </v-icon>
                </template>
                <span>{{ $t('opc.remover') }}</span>
            </v-tooltip>
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-icon
                        v-bind="attrs" v-on="on"
                        small
                        color="#246a73"
                        class="mr-2"
                        @click= "showItem(item)"
                    >
                        mdi-database
                    </v-icon>
                </template>
                <span>{{ $t('title.domain') }}</span>
            </v-tooltip>
        </template>      
        </v-data-table>
        <v-dialog v-model="picDialog" width="800px">
            <v-toolbar color="#2A3F54" dark>
                <h2>{{$t('navd.guser3')}}</h2>
             </v-toolbar>
            <v-card>
                <v-img v-bind:src="userPic" contain aspect-ratio="1.5"/>
            </v-card>
            <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                <v-btn color="#c9302c" dark @click="picDialog = false;" v-on="{ ...tooltip}">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                </template>
                <span>
                {{$t('indForm.close')}}
                </span>
            </v-tooltip>
        </v-dialog>
        <v-dialog v-model="cvDialog" width="800px">
            <v-toolbar color="#2A3F54" dark>
                <h1>{{$t('navd.guser2')}}</h1>
            </v-toolbar>
            <v-card>
                <template>
					{{page}}//{{pageCount}}
                    <pdf 
                        :src="cv"
                        :page="page"
                        @num-pages="pageCount = $event"	
                        @page-loaded="currentPage = $event"
                        style="width:700px"
                    ></pdf>
                </template>
								<v-btn color="#286090" dark @click="pageshift(-1)">
                    <v-icon>mdi-arrow-collapse-left</v-icon>
                </v-btn>
								<v-btn color="#286090" dark @click="pageshift(1)">
                    <v-icon>mdi-arrow-collapse-right</v-icon>
                </v-btn>
            </v-card>
            <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                <v-btn color="#c9302c" dark @click="cvDialog = false; page=1;" v-on="{ ...tooltip}">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                </template>
                <span>
                {{$t('indForm.close')}}
                </span>
            </v-tooltip>
        </v-dialog>
        <v-dialog
            v-model="deleteDialog"
            scrollable 
            width="500"
            persistent
        >
            <v-card>
                <v-toolbar color="#2A3F54" dark>
                    <h2>{{$t('navd.guser')}}</h2>
                </v-toolbar>
                <v-row>
                <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
                </v-col>
                <v-col>
                    <v-card-text>
                        <h3>{{$t('users.elim')}}</h3>
                    </v-card-text>
                </v-col>
                </v-row>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn class="mr-5" @click="deleteDialog = false;deleteItem(tempValue);" v-on="{ ...tooltip}">
                        <v-icon>mdi-check</v-icon>
                        </v-btn>
                    </template>
                    <span>
                        {{$t('navd.confirm')}}
                    </span>
                    </v-tooltip>
                    <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn @click="deleteDialog = false" v-on="{ ...tooltip}">
                        <v-icon>mdi-exit-to-app</v-icon>
                        </v-btn>
                    </template>
                    <span>
                        {{$t('navd.nao')}}
                    </span>
                    </v-tooltip>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog persistent v-model="dialog" max-width="800px">
            <userForm :value='value' :passedData='editedItem' @atualizarInfo=atualizarInfo($event) @emiteFecho=emiteFecho($event)></userForm>
        </v-dialog>
        <v-dialog v-model="noCVDialog" scrollable width="500" persistent>
            <v-card>
                <v-toolbar color="#2A3F54" dark>
                    <h1>{{$t('navd.guser')}}</h1>
                 </v-toolbar>
                <v-row>
                    <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                    </v-col>
                    <v-col>
                    <v-card-text>
                        <h3>{{$t('users.noCur')}}</h3>
                    </v-card-text>
                    </v-col>
                </v-row>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn color="#2A3F54" dark @click="noCVDialog = false" v-on="{ ...tooltip}">
                        <v-icon>mdi-exit-to-app</v-icon>
                        </v-btn>
                    </template>
                    <span>
                        {{$t('indForm.close')}}
                    </span>
                    </v-tooltip>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="noFoto" scrollable width="500" persistent>
            <v-card>
                <v-toolbar color="#2A3F54" dark>
                    <h1>{{$t('navd.guser')}}</h1>
                 </v-toolbar>
                <v-row>
                    <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                    </v-col>
                    <v-col>
                    <v-card-text>
                        <h3>{{$t('users.noFoto')}}</h3>
                    </v-card-text>
                    </v-col>
                </v-row>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn color="#2A3F54" dark @click="noFoto = false" v-on="{ ...tooltip}">
                        <v-icon>mdi-exit-to-app</v-icon>
                        </v-btn>
                    </template>
                    <span>
                        {{$t('indForm.close')}}
                    </span>
                    </v-tooltip>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="dialogShow" max-width="900px">
          <v-card>
            <v-app-bar color="#2A3F54" >
              <div class="d-flex align-center">
                <h3 width="40" class="white--text"> Domínios  </h3>
              </div>
            </v-app-bar>
            <v-container>
              <v-row>
    
                <v-col cols="8">
                  <dl>
                    <dt class="title">{{this.user._id}}</dt>
                    <dd class="ml-5">{{this.domain.header}}</dd>
                  </dl>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-expansion-panels focusable>
                    <v-expansion-panel
                      v-for="(item,i) in this.domain.dom"
                      :key="i"
                    >
                      <v-expansion-panel-header>Domínio {{i+1}}</v-expansion-panel-header>
                      <v-expansion-panel-content>
                      
                          <h4>Domínio:</h4> <span>{{item._id}}</span>
                          <h4>Descrição:</h4> <span>{{item.description}}</span>  
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
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
    </div>
</template>

<script>
import axios from 'axios'
import pdf from 'vue-pdf'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import UserForm from '../components/userForm.vue'
export default {
    data(){
        return{
            headers:[
                {
                    text: `${this.$t('users.id')}`,
                    align: 'start',
                    value: '_id'
                },
                {
                    text:`${this.$t('users.nome')}`,
                    value: 'name'
                },
                {
                    text:`${this.$t('users.email')}`,
                    value: 'email'
                },
                {
                    text:`${this.$t('users.tipo')}`,
                    value: 'type'
                },
                {
                    text:`${this.$t('users.opt')}`,
                    value:'options',
                    sortable: false
                }
            ],
            search:'',
            dialog: false,
            ajuda:'users',
            value:'',
            users:[],
            errors:[],
            editedIndex: -1,
            editedItem: {
                _id: '',
                name: '',
                email: '',
                dom: ''
            },
            domain: {
              _id: '',
              description: 'pt',
              body: [],
            },
            userPic:'',
            picDialog:false,
            cv:'',
            cvDialog:false,
            noCVDialog:false,
            noFoto: false,
            pageCount:0,
            currentPage:0,
            deleteDialog:false,
            tempValue:{},
            user:{},
            navDomains: [],
            dialogShow: false,
            page:1
        }
    },
    watch: {
        dialog (val) {
            val || this.close()
        },
    },
    components:{
        'appHeader': Header,
        'navDraw':NavDraw,
        'userForm':UserForm,
        'pdf':pdf
    },
    methods: {
      atualizarInfo: function(){
        this.dialog=false
        axios.get(`${process.env.VUE_APP_BACKEND}/users/users?type=responsible`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
          .then(response => {
            this.navDomains=response.data.domains
            var todos = response.data.users
            var domains = response.data.domains
            for(let i = 0; i<todos.length;i++){ 
                todos[i].dom = []
                for(let j = 0; j < domains.length; j++ ){
                    if(todos[i]._id === domains[j].responsible._id){
                        todos[i].dom.push(domains[j])
                    }
                } 
            }
            todos = todos.filter(item => item.dom.length !== 0)
            this.users = todos
        }).catch(e => {
            //console.log(e)
            this.errors.push(e)
        })
      },
      editItem (item, value) {
        this.editedIndex = this.users.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.value=value
        this.editedItem.tip = "responsible"
        //console.log("AAAAAAAAAAAAA")
        //console.log(this.value)
        //console.log(this.editedItem)
        this.dialog = true
      },
      verObjectItem(item,value){
        //console.log(item)
        const index = this.users.indexOf(item)
        //console.log(this.users[index])        
        if (value == 'curriculo'){
          axios.get(`${process.env.VUE_APP_BACKEND}/users/curriculo/${this.users[index]._id}?nome=${this.$store.state.user._id}&?seed=${Date.now()}&action=gestao&type=responsible  `, {
            responseType:'arraybuffer',
            headers: {
                'Authorization': `Bearer: ${this.$store.state.jwt}`
            }
          })
          .then(response => {
                var pdf = new Buffer(response.data, 'binary').toString('base64')
                this.cv = `data:${response.headers['content-type'].toLowerCase()};base64,${pdf}`
				this.cvDialog=true
          }).catch(e => {
              this.noCVDialog = true
              ////console.log(e)
              this.errors.push(e)
          })
        }
        else if(value == 'foto'){
            axios.get(`${process.env.VUE_APP_BACKEND}/users/foto/${this.users[index]._id}?nome=${this.$store.state.user._id}&?seed=${Date.now()}&action=gestao&type=responsible`, {
                responseType:'arraybuffer',
                headers: {
                    'Authorization': `Bearer: ${this.$store.state.jwt}`
                }
            })
            .then(response => {
                var image = new Buffer(response.data, 'binary').toString('base64')
                this.userPic = `data:${response.headers['content-type'].toLowerCase()};base64,${image}`
                this.picDialog = true
            }).catch(e => {
                this.noFoto = true
                //alert('Este utilizador não possui foto')
                //console.log(e)
                this.errors.push(e)
            })
        }
      },
      close () {
        this.dialog = false
        this.editedItem={}
        this.value='ver'
      },
    
    
    showItem (item) {
        console.log(item)
        this.domain = Object.assign({}, item)
        this.user = Object.assign({}, item)
        this.dialogShow = true
      },


      closeShow(){
        this.dialogShow = false
      },

      deleteItem (item) {
        const index = this.users.indexOf(item)
        //console.log('Index: ' + index + ' Username: ' + this.users[index]._id)
        axios.get(`${process.env.VUE_APP_BACKEND}/users/apagar/` + this.users[index]._id + `?nome=${this.$store.state.user._id}&type=responsible`,{ headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            var todos = response.data.users
            var domains = response.data.domains
            for(let i = 0; i<todos.length;i++){ 
                todos[i].dom = []
                for(let j = 0; j < domains.length; j++ ){
                    if(todos[i]._id === domains[j].responsible._id){
                        todos[i].dom.push(domains[j])
                    }
                } 
            }
            todos = todos.filter(item => item.dom.length !== 0)
            this.users = todos
        }).catch(e => {
            //console.log(e)
            this.errors.push(e)
        })
      },
        emiteFecho(){
            this.dialog=false
        },
        pageshift(shift){
            var temp = this.page + shift
            if (temp > 0 && temp <= this.pageCount){
                this.page=temp
            }
        }
    },
    created() {
                //console.log('store->' + this.$store.state.jwt)
        axios.get(`${process.env.VUE_APP_BACKEND}/users/users?nome=${this.$store.state.user._id}&type=responsible`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            var todos = response.data.users
            var domains = response.data.domains
            for(let i = 0; i<todos.length;i++){ 
                todos[i].dom = []
                for(let j = 0; j < domains.length; j++ ){
                    if(todos[i]._id === domains[j].responsible._id){
                        todos[i].dom.push(domains[j])
                    }
                } 
            }
            todos = todos.filter(item => item.dom.length !== 0)
            this.users = todos
            console.log(this.users)
        }).catch(e => {
            //console.log(e)
            this.errors.push(e)
        })
    }
}
</script>
<style scoped>
  .v-data-table /deep/ th{
        background-color:#4b779e;
    }
    .v-data-table /deep/ tr{
        color: #73879C;
        font-size: 13px;
    }
    .v-data-table /deep/ tr:nth-child(even){
        background-color: rgb(245, 245, 245);
    }
  #users *{
            box-sizing: border-box;
  }
  #users{
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
