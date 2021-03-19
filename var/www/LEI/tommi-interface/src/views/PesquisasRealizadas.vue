<template>
    <div id="pesquisas">
        <appHeader :ajuda='ajuda'></appHeader>
        <div v-if="this.$store.state.user.tipo === 'Admin'" >
            <navDraw></navDraw>
        </div>
        <div v-else>
            <navDrawLeitor></navDrawLeitor>
        </div>
        <v-data-table
            :headers="headers"
            :items="pesquisas"
            :items-per-page="15"
            :sort-by="['data']"
            :search="search"
            multi-sort            
        >
            <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title>{{$t('navd.estatisticas')}}</v-toolbar-title>
                    <v-divider
                    class="mx-4"
                    inset
                    vertical
                    ></v-divider>
                    <v-spacer></v-spacer>
                    <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Procura"
                        single-line
                        hide-details
                    ></v-text-field>
                </v-toolbar>
            </template>
            <template v-slot:header.pesquisa="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.folio="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.versao="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.resultado="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.data="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.hora="{ header }">
                <label> {{header.text}} </label>
            </template>
        </v-data-table>
    </div>
</template>
<script>
import axios from 'axios'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
export default {
    data(){
        return{
            headers:[
                {
                    text: `${this.$t('pr.pesq')}`,
                    align: 'start',
                    value: 'pesquisa'
                },
                {
                    text:`${this.$t('pr.fol')}`,
                    value: 'folio'
                },
                {
                    text:`${this.$t('pr.ver')}`,
                    value: 'versao'
                },
                {
                    text:`${this.$t('pr.pesq')}`,
                    value: 'resultado'
                },
                {
                    text:`${this.$t('pr.d')}`,
                    value: 'data'
                },
                {
                    text:`${this.$t('pr.h')}`,
                    value:'hora'
                }
            ],
            search:'',
            ajuda:'pesquisas',
            pesquisas:[],
            errors:[],
            item:{}
        }
    },
    // watch: {
    //     dialog (val) {
    //         val || this.close()
    //     },
    // },
    components:{
        'appHeader': Header,
        'navDrawLeitor':navDrawLeitor,
        'navDraw':NavDraw
    },
    // methods:{
    //     close () {
    //     this.dialog = false
    //     this.item={}
    //     },
    //     emiteFecho: function(){
    //     this.dialog=false
    //     }
    // },
    created() {
        axios.get(`https://tommi2.di.uminho.pt/api/folios/pesquisas?nome=${this.$store.state.user._id}`,{headers:{
          Authorization:`Bearer: ${this.$store.state.jwt}`
        }})
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            this.pesquisas = response.data.pesquisas
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
    label {
        color: white;
        padding: 8px;
        font-family: Arial, sans-serif;
        font-weight: bold;
        font-size: 15px;
    }
    #pesquisas *{
            box-sizing: border-box;
    }
    #pesquisas{
            margin: 20px auto;
            max-width: 1100px;
            margin-bottom: 80px;
    }
</style>
