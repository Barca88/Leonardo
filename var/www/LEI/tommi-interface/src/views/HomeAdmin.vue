<template>
    <div id="homeAdmin" style="width:70%">
        <appHeader></appHeader>
        <navDraw></navDraw>
        <div >
            <v-toolbar flat style="margin-top:2.5cm;margin-bottom:2.5cm">
                <v-row>
                    <v-col>
                        <v-card class="text-center ml-10 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-folder-open</v-icon>{{$t('hAdmin.f')}}</h4>
                                <h2 style="color:blue"><b>{{nFolios}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-divider vertical></v-divider>
                    <v-col>
                        <v-card class="text-center ml-5 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-folder-open</v-icon>{{$t('hAdmin.doc')}}</h4>
                                <h2 style="color:blue"><b>{{nDocs}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-divider vertical></v-divider>
                    <v-col>
                        <v-card class="text-center ml-5 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-format-list-bulleted-square</v-icon>{{$t('hAdmin.ind')}}</h4>
                                <h2 style="color:green"><b>{{nInds}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-divider vertical></v-divider>
                    <v-col>
                        <v-card class="text-center ml-5 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-note-multiple</v-icon>{{$t('hAdmin.tag')}}</h4>
                                <h2 style="color:green"><b>{{nTags}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-divider vertical></v-divider>
                    <v-col>
                        <v-card class="text-center ml-5 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-format-list-bulleted-square</v-icon>{{$t('hAdmin.pal')}}</h4>
                                <h2 style="color:green"><b>{{nPals}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-divider vertical></v-divider>
                    <v-col>
                        <v-card class="text-center ml-5 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-account-multiple</v-icon>{{$t('hAdmin.users')}}</h4>
                                <h2 style="color:blue"><b>{{nUsers}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-toolbar>
        </div>
        <div class="mt-12">
            <h3 class="ml-10 mt-6">{{"Foram inseridos " + percent + "% dos fólios na última semana"}}</h3>
            <v-row>
                <v-col>
                    <v-card color="#2A3F54" dark class="text-center ml-10 mt-6 mr-10">
                        <v-card-text>
                            <h2>{{$t('hAdmin.ins')}}</h2>
                        </v-card-text>
                    </v-card>
                    <v-card class="ml-10 mt-6 mr-10" v-if="condition==true">
                        <v-card-actions>
                            <v-sparkline
                                :labels="labels"
                                :value="number"
                                label-size="3"
                                color="red"
                                line-width="2"
                                padding="16"
                            ></v-sparkline>
                        </v-card-actions>
                    </v-card>
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
            nFolios:0,
            nDocs:0,
            nInds:0,
            nTags:0,
            nPals:0,
            nUsers:0,
            value:[],
            labels:[],
            number:[],
            percent:0,
            condition:false,
        }
    },
    components:{
            'appHeader': Header,
            'navDraw':NavDraw
    },
    created: async function() {
        //Data atual
        var today = new Date()
        var date = (today.getMonth()+1) + '/' + today.getDate() + '/' + today.getFullYear()
        var dateTime = new Date(date).getTime()
        for(let i = -14;i<=0;i++){
            let last = new Date(dateTime + (i * 24 * 60 * 60 * 1000));
            let day =last.getDate();
            if(day <= 9)
                day = '0' + day;
            let month=last.getMonth()+1;
            if(month <= 9)
                month = '0' + month;
            let year=last.getFullYear();
            let label = (month + '/' + day + '/' + year)
            this.labels.push(label)
        }
        //Users
        axios.get(`https://tommi2.di.uminho.pt/api/users/users?nome=${this.$store.state.user._id}`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            this.nUsers = response.data.users.length
        }).catch(e => {
            this.errors.push(e)
        })


        //Fólios
        await axios.get(`https://tommi2.di.uminho.pt/api/folios/folios?nome=${this.$store.state.user._id}`,{headers:{
            Authorization:`Bearer: ${this.$store.state.jwt}`
            }})
            .then(response => {
                this.nFolios = response.data.folios.length
                for(let i = 0; i<response.data.folios.length; i++){
                    let data = response.data.folios[i].data
                    let dataArray = data.split(/[\s-:]+/)
                    let comparableData = dataArray[1] + '/' + dataArray[2] + '/' + dataArray[0]
                    this.value.push(comparableData)
                }
                //para ja nao ha mais documentos?
                this.nDocs = response.data.folios.length
            }).catch(e => {
                this.errors.push(e)
        })
        await this.contains()
        //Tags
        axios.get(`https://tommi2.di.uminho.pt/api/folios/tags?nome=${this.$store.state.user._id}`,{headers:{
          Authorization:`Bearer: ${this.$store.state.jwt}`
        }})
        .then(response => {
            this.nTags = response.data.tags.length
        }).catch(e => {
            this.errors.push(e)
        })
        //Índices
        axios.get(`https://tommi2.di.uminho.pt/api/folios/index?nome=${this.$store.state.user._id}`,{headers:{
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`
        }})
        .then(response => {
            this.nInds = response.data.indexs.length
            let total = 0
            for(let i = 0; i<response.data.indexs.length;i++){
                total +=response.data.indexs[i].n_ocorrencias
            }
            this.nPals = total
        }).catch(e => {
            this.errors.push(e)
        })
    },
    methods:{
        contains: function(){
            for(let i = 0;i<this.labels.length;i++){
                this.number[i] = this.getOccurrence(this.value,this.labels[i])
            }
            this.percent = ((this.number.reduce((a, b) => a + b, 0)/this.nFolios)*100).toPrecision(4)
            this.condition = true
        },
        getOccurrence: function(array, value) {
            var count = 0;
            array.forEach((v) => (v === value && count++));
            return count;
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
    label {
        color: white;
        padding: 8px;
        font-family: Arial, sans-serif;
        font-weight: bold;
        font-size: 15px;
    }
    #homeAdmin *{
            box-sizing: border-box;
    }
    #homeAdmin{
                margin: 20px auto;
                margin-bottom: 80px;
    }
</style>