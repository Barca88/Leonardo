<template>
    <div id="usersImport">
        <v-main class="pa-10">
            <h4 class="text-h4 mb-4">
                Importação de Dados de Utilizador
            </h4>

            <v-main>
                <v-row no-gutters align="center" justify>
                    <v-col
                        cols="12"
                        sm="2"
                        md="1"
                    >
                        <span>
                            Ficheiro: 
                        </span>
                    </v-col>
                    <v-col
                        cols="12"
                        sm="5"
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
                        <v-btn  v-on="{ ...tooltip}" @click="onFileChanged()" class="mr-5" dark color = "amber lighten">
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
                
            </v-main>
                
                
        </v-main>
        <v-snackbar
            v-model="snackbar"
            timeout="-1"
        >
            Pedidos de Utilizadores adicionados com sucesso

            <template v-slot:action="{ attrs }">
                
                <v-btn
                color="green"
                text
                v-bind="attrs"
                @click="snackbar = false; $router.push('/pedidos')"

                >
                Continuar
                </v-btn>
                <v-btn
                color="pink"
                text
                v-bind="attrs"
                @click="snackbar = false"
                >
                Fechar
                </v-btn>
            </template>
        </v-snackbar>
    </div>
</template>
<script>
import axios from 'axios'
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
            file: "",
            snackbar: false
        }
    },
    methods: {
        onFileChanged() {
            this.selectedFile = this.file

            // console.log(this.file)
            
            let formData = new FormData()
            formData.append('registos',this.selectedFile)
            axios.post(`${process.env.VUE_APP_BACKEND}/users/import_registos`,formData,{
                responseType:'arraybuffer',
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`
                }
                }).then(() => {
                    this.snackbar=true
                }).catch(e => {
                    this.errors.push(e)
                })
        },
    },
    //Active
    created:function(){
        axios.get(`${process.env.VUE_APP_BACKEND}/users/active?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
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
</style>