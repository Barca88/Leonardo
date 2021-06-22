<template>
    <div id="usersImport">
        <appHeader></appHeader>
        <navDraw></navDraw>
        <v-container class="pa-10">
            <h4 class="text-h4 mb-4">
                Importação de Dados de Utilizador
            </h4>

            <v-container>
                <v-row no-gutters>
                    <v-col
                        cols="12"
                        sm="6"
                        md="8"
                    >
                        <v-file-input
                            truncate-length="150"
                            show-size
                            v-model="file"
                            :clearable="false"
                            label="<ficheiro .csv>"
                        ></v-file-input>
                    </v-col>
                    
                </v-row>
                <v-row no-gutters>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                        <v-btn  v-on="{ ...tooltip}" class="mr-5" dark color = "amber lighten">
                            <v-icon>mdi-checkbox-marked-outline</v-icon>
                        </v-btn>
                        </template>
                        <span>
                            Confirmar
                        </span>
                    </v-tooltip>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                        <v-btn  v-on="{ ...tooltip}" @click="file=''"  class="mr-5" dark color = "green accent-3">
                            <v-icon>mdi-broom</v-icon>
                        </v-btn>
                        </template>
                        <span>
                            Limpar
                        </span>
                    </v-tooltip>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                        <v-btn  v-on="{ ...tooltip}" class="mr-5" dark color = "blue-grey darken-4">
                            <v-icon>mdi-help</v-icon>
                        </v-btn>
                        </template>
                        <span>
                            Ajuda
                        </span>
                    </v-tooltip>
                </v-row>
                
            </v-container>
                
                
        </v-container>
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
            ],
            file: ""
        }
    },
    components:{
            'appHeader': Header,
            'navDraw': NavDraw
    },
    methods: {
        onButtonClick(up) {
            this.isSelecting = true
            window.addEventListener('focus', () => {
                this.isSelecting = false
            }, { once: true })

            if (up==='uploaderpic'){
                this.$refs.uploaderpic.click()
            }
            else if (up==='uploadercv'){
                this.$refs.uploadercv.click()
            }
        },
        onFileChanged(e) {
            this.selectedFile = e.target.files[0]
            
            let formData = new FormData()
            formData.append('registos',this.selectedFile)
            axios.post(`http://localhost:5000/users/importcsv/`,formData,{
                responseType:'arraybuffer',
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`
                }
                }).then(response => {
                    var pdf = new Buffer(response.data, 'binary').toString('base64')
                    this.cv = `data:${response.headers['content-type'].toLowerCase()};base64,${pdf}`
                }).catch(e => {
                    this.errors.push(e)
                })
        },
    }
    //Active
    created:function(){
        axios.get(`https://localhost:5000/users/active?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
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
    .container {
        margin: 20px auto 80px auto;
        max-width: 1100px;
    }
</style>