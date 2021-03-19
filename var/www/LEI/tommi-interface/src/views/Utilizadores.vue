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
                <v-toolbar-title>{{$t('users.title')}}</v-toolbar-title>
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
                <v-dialog persistent v-model="dialog" max-width="800px">
                    <template v-slot:activator="{ on }">
                        <v-btn color="#2A3F54" dark class="mb-2" v-on="on" @click="editItem({}, 'adicionar')">
                            <v-icon>mdi-account-plus</v-icon>
                        </v-btn>
                    </template>
                    <userForm :value='value' :passedData='editedItem' @atualizarInfo=atualizarInfo($event) @emiteFecho=emiteFecho($event)></userForm>
                </v-dialog>
            </v-toolbar>
        </template>
        <template v-slot:header._id="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.nome="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.email="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.tipo="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.options="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:item.options="{ item }">
            <v-icon
                small
                class="mr-2"
                @click="editItem(item, 'ver')"
            >
                mdi-eye
            </v-icon>
            <v-icon
                small
                class="mr-2"
                @click="editItem(item,'editar')"
            >
                mdi-pencil
            </v-icon>
            <v-icon
                small
                class="mr-2"
                @click="verObjectItem(item,'curriculo')"
            >
                mdi-file-pdf
            </v-icon>
            <v-icon
                small
                class="mr-2"
                @click="verObjectItem(item,'foto')"
            >
                mdi-camera
            </v-icon>
            <v-icon
                small
                @click="deleteDialog = true;tempValue=item"
            >
                mdi-trash-can
            </v-icon>
        </template>
        </v-data-table>
        <v-dialog v-model="picDialog" width="800px">
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
        <v-dialog v-model="noCVDialog" scrollable width="500" persistent>
            <v-card>
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
                    value: 'nome'
                },
                {
                    text:`${this.$t('users.email')}`,
                    value: 'email'
                },
                {
                    text:`${this.$t('users.tipo')}`,
                    value: 'tipo'
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
                nome: '',
                email: '',
                tipo: ''
            },
            userPic:'',
            picDialog:false,
            cv:'',
            cvDialog:false,
            noCVDialog:false,
            pageCount:0,
            currentPage:0,
            deleteDialog:false,
            tempValue:{},
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
        axios.get(`https://tommi2.di.uminho.pt/api/users/users?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
          .then(response => {
            // JSON responses are automatically parsed.
            var todos = response.data.users
            for(let i = 0; i<todos.length;i++){
                if(todos[i]._id === this.$store.state.user._id){
                    todos.splice(i,1)
                }
            }
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
          axios.get(`https://tommi2.di.uminho.pt/api/users/curriculo/${this.users[index]._id}?seed=${Date.now()}`, {
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
            axios.get(`https://tommi2.di.uminho.pt/api/users/foto/${this.users[index]._id}?seed=${Date.now()}`, {
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
                alert('Este utilizador não possui foto')
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
      edit(){
        this.update = true
        axios.get(`https://tommi2.di.uminho.pt/api/users/users?nome=admin`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
          .then(response => {
              // JSON responses are automatically parsed.
              //console.log(response.data)
              this.users = response.data.users
          }).catch(e => {
              //console.log(e)
              this.errors.push(e)
        })
        this.update = false
      },

      deleteItem (item) {
        const index = this.users.indexOf(item)
        //console.log('Index: ' + index + ' Username: ' + this.users[index]._id)
        axios.get(`https://tommi2.di.uminho.pt/api/users/apagar/` + this.users[index]._id + `?nome=` + this.users[index].username,{ headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            this.users = response.data.users
            this.tempValue = {}
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
        axios.get(`https://tommi2.di.uminho.pt/api/users/users?nome=admin`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            var todos = response.data.users
            for(let i = 0; i<todos.length;i++){
                if(todos[i]._id === this.$store.state.user._id){
                    todos.splice(i,1)
                }
            }
            this.users = todos
            //console.log(this.users)
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
