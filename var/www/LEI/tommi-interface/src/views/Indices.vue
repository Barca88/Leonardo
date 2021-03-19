<template>
    <div id="indices">
        <div>
            <appHeader :ajuda='ajuda'></appHeader>
        </div>
        <div v-if="this.$store.state.user.tipo === 'Admin'" >
            <navDraw></navDraw>
        </div>
        <div v-else>
            <navDrawLeitor></navDrawLeitor>
        </div>
        <v-data-table
            :headers="headers"
            :items="indices"
            :items-per-page="15"
            :sort-by="['_id']"
            :search="search"
            multi-sort            
        >
            <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title>{{$t('ind.title')}}</v-toolbar-title>
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
                    ></v-text-field>
                    <v-dialog persistent v-model="dialog" max-width="500px">
                        <indexForm :passedData='item' @emiteFecho=emiteFecho($event)></indexForm>
                    </v-dialog>
                </v-toolbar>
            </template>
            <template v-slot:header._id="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.n_ocorrencias="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.ref="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.options="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:item.ref="{ item }">
                <ul v-for="i in item.ref" :key="i">
                    <li>{{i}}</li>
                </ul>
            </template>
            <template v-slot:item.options="{ item }">
                <v-icon
                    small
                    class="mr-2"
                    @click="editItem(item)"
                >
                    mdi-eye
                </v-icon>
            </template>
        </v-data-table>
    </div>
</template>
<script>
import axios from 'axios'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
import indexForm from '../components/indexForm.vue'
export default {
    data(){
        return{
            headers:[
                {
                    text: `${this.$t('ind.pal')}`,
                    align: 'start',
                    value: '_id'
                },
                {
                    text:`${this.$t('ind.oco')}`,
                    value: 'n_ocorrencias'
                },
                {
                    text:`${this.$t('ind.fol')}`,
                    value: 'ref'
                },
                {
                    text:`${this.$t('ind.opt')}`,
                    value:'options',
                    sortable: false
                }
            ],
            search:'',
            ajuda:'indices',
            indices:[],
            errors:[],
            dialog: false,
            item:{}
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
        'indexForm':indexForm
    },
    methods:{
        editItem (item) {
            this.item=item
            this.dialog = true
      },
      close () {
        this.dialog = false
        this.item={}
      },
      emiteFecho:function(){
          this.dialog=false
      }
    },
    created() {
        axios.get(`https://tommi2.di.uminho.pt/api/folios/index?nome=${this.$store.state.user._id}`,{headers:{
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`
        }})
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            this.indices = response.data.indexs
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
    #indices *{
            box-sizing: border-box;
    }
    #indices{
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
