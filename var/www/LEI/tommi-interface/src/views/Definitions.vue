<template>
    <div id="definitions">
        <appHeader :ajuda='ajuda'></appHeader>
        <div v-if="this.$store.state.user.tipo === 'Admin'" >
            <navDraw></navDraw>
        </div>
        <div v-else>
            <navDrawLeitor></navDrawLeitor>
        </div>
        <v-data-table
            :headers="headers"
            :items="definitions"
            :items-per-page="15"
            :sort-by="['_id']"
            :search="search"
            class="mytable"
            multi-sort     
        ><template v-slot:top>
            <v-toolbar flat color="white">
                <v-toolbar-title>{{$t('def.title')}}</v-toolbar-title>
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
                <v-dialog persistent v-model="dialog" max-width="500px">
                    <template v-slot:activator="{ on }">
                        <v-btn  v-if="$store.state.user.tipo === 'Admin'" color="#2A3F54" dark class="mb-2" v-on="on" @click="editItem({}, 'adicionar')"><v-icon>mdi-plus</v-icon></v-btn>
                    </template>
                    <definitionForm :value='value' :passedData='editedItem' @atualizarInfo=atualizarInfo($event) @emiteFecho=emiteFecho($event)></definitionForm>
                </v-dialog>
            </v-toolbar>
        </template>
        <template v-slot:header._id="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.desc="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.wac="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.tag="{ header }">
            <label> {{header.text}} </label>
        </template>
        <template v-slot:header.exemplo="{ header }">
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
            <v-icon v-if="$store.state.user.tipo === 'Admin'"
                small
                @click="deleteDialog = true;tempValue=item"
            >
                mdi-trash-can
            </v-icon>
        </template>
        </v-data-table>
        <v-dialog
            v-model="deleteDialog"
            scrollable 
            width="500"
            persistent
        >
            <v-card>
                <v-row>
                <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
                </v-col>
                <v-col>
                    <v-card-text>
                        <h3>{{$t('def.elim')}}</h3>
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
    </div>
</template>

<script>
import axios from 'axios'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
import definitionForm from '../components/definitionForm.vue'
export default {
    data(){
        return{
            headers:[
                {
                    text: `${this.$t('def.elem')}`,
                    align: 'start',
                    value: '_id'
                },
                {
                    text:`${this.$t('def.desc')}`,
                    value: 'desc'
                },
                {
                    text:`${this.$t('def.wac')}`,
                    value: 'wac'
                },
                {
                    text:`${this.$t('def.tagHTML')}`,
                    value: 'tag'
                },
                {
                    text:`${this.$t('def.ex')}`,
                    value: 'exemplo'
                },
                {
                    text:`${this.$t('def.opt')}`,
                    value:'options',
                    sortable: false
                }
            ],
            search:'',
            dialog: false,
            ajuda:'definitions',
            value:'',
            definitions:[],
            errors:[],
            editedIndex: -1,
            deleteDialog:false,
            tempValue:{},
            editedItem: {
                _id: '',
                desc: '',
                wac: '',
                tag: '',
                exemplo: '',
                procura:''
            }
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
        'navDrawLeitor':navDrawLeitor,
        'definitionForm':definitionForm
    },
    methods: {
      atualizarInfo: function(){
        this.dialog=false
        this.onUpdate()
      },
      emiteFecho:function(){
        this.dialog=false
      },
      editItem (item, value) {
        this.editedIndex = this.definitions.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.value=value
        //console.log("AAAAAAAAAAAAA")
        //console.log(this.value)
        //console.log(this.editedItem)
        this.dialog = true
      },
      close () {
        this.dialog = false
        this.editedItem={}
        this.value='ver'
      },
      onUpdate(){
          axios.get(`https://tommi2.di.uminho.pt/api/settings/ver?nome=admin`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
          .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            this.definitions = response.data.settings
            //console.log('Definitions: ' + this.definitions)
          }).catch(e => {
            //console.log(e)
            this.errors.push(e)
        })
      },

      deleteItem (item) {
        const index = this.definitions.indexOf(item)
        //console.log('Index: ' + index + ' elemento: ' + this.definitions[index]._id)
        axios.get(`https://tommi2.di.uminho.pt/api/settings/apagar/` + this.definitions[index]._id + `?nome=` + this.definitions[index].elemento,{ headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            this.definitions = response.data.settings
            this.tempValue = {}
        }).catch(e => {
            //console.log(e)
            this.errors.push(e)
        })
      }
    },
    created() {
      //console.log('store->' + this.$store.state.jwt)
      this.onUpdate()
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
    #definitions *{
            box-sizing: border-box;
    }
    #definitions{
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
