<template>
    <div id="historial">
        <appHeader></appHeader>
        <div v-if="this.$store.state.user.tipo === 'Admin'" >
            <navDraw></navDraw>
        </div>
        <v-data-table
            :headers="headers"
            :items="active"
            :items-per-page="15"
            :sort-by="['stamp','user']"
            :sort-desc="[true,false]"
            :search="search"
            multi-sort
        >
            <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title>{{$t('hist.haccess')}}</v-toolbar-title>
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
                        <template v-slot:activator="{ on: tooltip }">
                        <v-btn color="#2A3F54" dark class="mb-2" @click="dialog = true" v-on="{ ...tooltip}">
                            <v-icon>mdi-trash-can</v-icon>
                        </v-btn>
                        </template>
                        <span>
                            {{$t('hist.cleanH')}}
                        </span>
                    </v-tooltip>
                    <v-dialog
                        v-model="dialog"
                        scrollable 
                        width="500"
                        persistent
                    >
                        <v-card>
                            <v-toolbar color="#2A3F54" dark>
                                <h1>{{$t('hist.haccess')}}</h1>
                            </v-toolbar>
                            <v-row>
                            <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                                <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
                            </v-col>
                            <v-col>
                                <v-card-text>
                                <h3>{{$t('hist.elim')}}</h3>
                                </v-card-text>
                            </v-col>
                            </v-row>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on: tooltip }">
                                    <v-btn @click="dialog = false;eliminarHistorico()" v-on="{ ...tooltip}" class="mr-5">
                                        <v-icon>mdi-check</v-icon>
                                    </v-btn>
                                    </template>
                                    <span>
                                    {{$t('navd.confirm')}}
                                    </span>
                                </v-tooltip>
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on: tooltip }">
                                    <v-btn @click="dialog = false" v-on="{ ...tooltip}">
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
                </v-toolbar>
            </template>
            <template v-slot:header.stamp="{ header }">
                <label> {{header.text}} </label>
            </template>
            <template v-slot:header.user="{ header }">
                <label> {{header.text}} </label>
            </template>
             <template v-slot:header.request="{ header }">
                <label> {{header.text}} </label>
            </template>
        </v-data-table>
    </div>
</template>
<script>
import axios from 'axios'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'

export default {
    data(){
        return{
            active:[],
            dialog:false,
            search:'',
            headers:[
                {
                    text:`${this.$t('hist.adate')}`,
                    value: 'stamp',
                    align:'start'
                },
                { 
                    text:`${this.$t('users.nome')}`,
                    value: 'user'
                },
                {
                    text:`${this.$t('hist.req')}`,
                    value: 'request'
                }
            ]
        }
    },
    components:{
        'appHeader': Header,
        'navDraw':NavDraw
    },
    created: async function() {
        //Active
        axios.get(`https://tommi2.di.uminho.pt/api/users/history?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            this.active = response.data.reqs

        }).catch(e => {
            this.errors.push(e)
        })
    },
    methods:{
        eliminarHistorico:function(){
            axios.get(`https://tommi2.di.uminho.pt/api/users/historyCleanse?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
            .then(response => {
                this.active=response.data.history

            }).catch(e => {
                this.errors.push(e)
            })
        }
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
  #historial *{
            box-sizing: border-box;
  }
  #historial{
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