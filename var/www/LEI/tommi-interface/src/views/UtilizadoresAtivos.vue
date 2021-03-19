<template>
    <div id="uAtivos">
        <appHeader></appHeader>
        <navDraw></navDraw>
        <div>
            <v-row>
                <v-col>
                    <v-container style="width:60%">
                            <v-data-table
                                :headers="headers"
                                :items="active"
                                :sort-by="['_id']"
                                :search="search"
                                :items-per-page="15"
                                multi-sort       
                            >
                            <template v-slot:top>
                                <v-toolbar flat color="white">
                                    <v-toolbar-title>{{$t('navd.uativo')}}</v-toolbar-title>
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
                                        class="mr-5"
                                    ></v-text-field>
                                </v-toolbar>
                            </template>
                            <template v-slot:header._id="{ header }">
                                <label> {{header.text}} </label>
                            </template>
                            <template v-slot:header.stamp="{ header }">
                                <label> {{header.text}} </label>
                            </template>
                            </v-data-table>
                    </v-container>
                </v-col>
            </v-row>
        </div>
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
            headers:[
                { 
                    text:`${this.$t('users.nome')}`,
                    value: '_id'
                },
                {
                 text:`${this.$t('hist.adate')}`,
                    value: 'stamp'
                }
            ]
        }
    },
    components:{
            'appHeader': Header,
            'navDraw':NavDraw
    },
    //Active
    created:function(){
        axios.get(`https://tommi2.di.uminho.pt/api/users/active?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            this.active = response.data.users

        }).catch(e => {
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
    #uAtivos *{
            box-sizing: border-box;
    }
    #uAtivos{
                margin: 20px auto;
                margin-bottom: 80px;
    }
</style>