<template>
    <div id="pedidos">
        <appHeader :ajuda='ajuda'></appHeader>
        <navDraw></navDraw>
        <v-data-table
            :headers="headers"
            :items="pedidos"
            :items-per-page="15"
            :sort-by="['_id']"
            :search="search"
            multi-sort       
        ><template v-slot:top>
            <v-toolbar flat color="white">
                <v-toolbar-title>{{$t('navd.pedidos')}}</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    :label="`${$t('navd.se')}`"
                    single-line
                    hide-details
                ></v-text-field>
                <v-dialog 
                    persistent 
                    v-model="dialog" 
                    max-width="500px"
                >
                    <pedidoForm 
                        :value='value' 
                        :passedData='editedItem' 
                        @atualizarInfo=atualizarInfo($event) 
                        @emiteFecho=emiteFecho($event)
                    ></pedidoForm>
                </v-dialog>
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
                        @click="deleteDialog = true;tempValue=item"
                    >
                        mdi-trash-can
                    </v-icon>
                </template>
                <span>{{ $t('opc.remover') }}</span>
            </v-tooltip>
        </template>
        </v-data-table>
        <v-dialog v-model="picDialog" width="800px">
            <v-toolbar color="#2A3F54" dark>
                <h2>{{$t('navd.puser3')}}</h2>
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
            <v-card>
                <v-toolbar color="#2A3F54" dark>
                    <h1>{{$t('navd.puser2')}}</h1>
                </v-toolbar>
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
                    <h2>{{$t('navd.pedidos')}}</h2>
                </v-toolbar>
                <v-row>
                <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
                </v-col>
                <v-col>
                    <v-card-text>
                        <h3>{{$t('pedac.elim')}}</h3>
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
                <v-toolbar color="#2A3F54" dark>
                    <h2>{{$t('navd.pedidos')}}</h2>
                </v-toolbar>
                <v-row>
                    <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                    </v-col>
                    <v-col>
                    <v-card-text>
                        <h3>{{$t('pedac.noCur')}}</h3>
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
        <v-dialog v-model="noPicDialog" width="500px">
            <v-card>
                <v-toolbar color="#2A3F54" dark>
                    <h2>{{$t('navd.pedidos')}}</h2>
                </v-toolbar>
                <v-row>
                    <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                    </v-col>
                    <v-col>
                    <v-card-text>
                        <h3>{{$t('pedac.noPicText')}}</h3>
                    </v-card-text>
                    </v-col>
                </v-row>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn @click="noPicDialog = false" v-on="{ ...tooltip}">
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
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import pdf from 'vue-pdf'
import PedidoForm from '../components/pedidoForm.vue'
export default {
    data(){
        return{
            headers:[
                {
                    text: `${this.$t('pedac.id')}`,
                    align: 'start',
                    value: '_id'
                },
                {
                    text:`${this.$t('pedac.nome')}`,
                    value: 'name'
                },
                {
                    text:`${this.$t('pedac.email')}`,
                    value: 'email'
                },
                {
                    text:`${this.$t('pedac.tipo')}`,
                    value: 'type'
                },
                {
                    text:`${this.$t('pedac.opt')}`,
                    value:'options',
                    sortable: false
                }
            ],
            search:'',
            dialog: false,
            ajuda:'pedidos',
            value:'',
            pedidos:[],
            errors:[],
            editedIndex: -1,
            editedItem: {
                _id: '',
                name: '',
                email: '',
                type: ''
            },
            userPic:'',
            picDialog:false,
            noPicDialog:false,
            cv:'',
            cvDialog:false,
            pageCount:0,
            currentPage:0,
            noCVDialog:false,
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
        'pedidoForm':PedidoForm,
        'pdf':pdf
    },
    methods: {
        atualizarInfo: function(){
            this.dialog = false
            axios.get(`${process.env.VUE_APP_BACKEND}/users/pedidos?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
            .then(response => {
                // JSON responses are automatically parsed.
                //console.log(response.data)
                this.pedidos = response.data.pedidos
            }).catch(e => {
                //console.log(e)
                this.errors.push(e)
            })
        },
        emiteFecho(){
            this.dialog = false
        },
        editItem (item, value) {
            this.editedIndex = this.pedidos.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.value=value
            //console.log("AAAAAAAAAAAAA")
            //console.log(this.value)
            //console.log(this.editedItem)
            this.dialog = true
        },
        verObjectItem(item,value){
            //console.log(item)
            const index = this.pedidos.indexOf(item)
            //console.log(this.pedidos[index])        
            if (value == 'curriculo'){
            axios.get(`${process.env.VUE_APP_BACKEND}/users/pedidos/curriculo/${this.pedidos[index]._id}?nome=${this.$store.state.user._id}&?seed=${Date.now()}`, {
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
                axios.get(`${process.env.VUE_APP_BACKEND}/users/pedidos/foto/${this.pedidos[index]._id}?nome=${this.$store.state.user._id}&?seed=${Date.now()}`, {
                    responseType:'arraybuffer',
                    headers: {
                        'Authorization': `Bearer: ${this.$store.state.jwt}`
                    }
                })
                .then(response => {
                    var image = new Buffer(response.data, 'binary').toString('base64')
                    this.userPic = `data:${response.headers['content-type'].toLowerCase()};base64,${image}`
                    this.picDialog=true
                }).catch(e => {
                    this.noPicDialog = true
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
            axios.get(`${process.env.VUE_APP_BACKEND}/users/pedidos?nome=admin`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
            .then(response => {
                // JSON responses are automatically parsed.
                //console.log(response.data)
                this.pedidos = response.data.pedidos
            }).catch(e => {
                //console.log(e)
                this.errors.push(e)
            })
            this.update = false
        },

        deleteItem (item) {
            let index = this.pedidos.indexOf(item)
            //console.log('Index: ' + index + ' Username: ' + this.pedidos[index]._id)
            axios.get(`${process.env.VUE_APP_BACKEND}/users/pedidos/apagar/` + this.pedidos[index]._id + `?nome=${this.$store.state.user._id}`,{ headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
            .then(response => {
                // JSON responses are automatically parsed.
                //console.log(response.data)
                this.pedidos = response.data.pedidos
                this.tempValue = {}
            }).catch(e => {
                //console.log(e)
                this.errors.push(e)
            })
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
      axios.get(`${process.env.VUE_APP_BACKEND}/users/pedidos?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
      .then(response => {
          // JSON responses are automatically parsed.
          //console.log(response.data)
          this.pedidos = response.data.pedidos
          console.log(this.pedidos)
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
  #pedidos *{
            box-sizing: border-box;
  }
  #pedidos{
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
