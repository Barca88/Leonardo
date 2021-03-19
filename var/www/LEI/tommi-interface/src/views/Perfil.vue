<template>
    <div id="perfil">
        <appHeader :ajuda='ajuda'></appHeader>
        <div v-if="this.$store.state.user.tipo === 'Admin'" >
            <navDraw></navDraw>
        </div>
        <div v-else>
            <navDrawLeitor></navDrawLeitor>
        </div>
        <v-container fluid style="margin-top:2.5cm">
            <v-row justify="space-around">
                <v-col cols="5">
                    <div class="title mb-1">{{$t('perfil.foto')}}</div>
                    <v-img v-bind:src="userPic" contain aspect-ratio="0.9"/>
                    <v-col>
                        <v-btn
                            color="#2A3F54"
                            dark
                            depressed
                            @click="onButtonClick('uploaderpic')"
                        >
                            {{$t('perfil.atuapic')}}
                        </v-btn>
                    </v-col>
                    <input
                        ref="uploaderpic"
                        class="d-none"
                        type="file"
                        accept="image/*"
                        @change="onPicChanged"
                    >
                </v-col>
                <v-col cols="5">
                    <v-simple-table class="table" >
                        <template v-slot:default>
                            <tbody>
                                <tr>
                                    <td class="text-left">{{$t('perfil.nome')}}</td>
                                    <td>
                                        <v-layout justify-center>
                                            {{nome}}
                                        </v-layout>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="text-left">{{$t('perfil.email')}}</td>
                                    <td>
                                        <v-layout justify-center>
                                            {{email}}
                                        </v-layout>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="text-left">{{$t('perfil.tipo')}}</td>
                                    <td>
                                        <v-layout justify-center>
                                            {{tipo}}
                                        </v-layout>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="text-left">{{$t('perfil.uni')}}</td>
                                    <td>
                                        <v-layout justify-center>
                                            {{universidade}}
                                        </v-layout>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="text-left">{{$t('perfil.dep')}}</td>
                                    <td>
                                        <v-layout justify-center>
                                            {{departamento}}
                                        </v-layout>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="text-left">{{$t('perfil.data')}}</td>
                                    <td>
                                        <v-layout justify-center>
                                            {{data}}
                                        </v-layout>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="text-left">{{$t('perfil.obs')}}</td>
                                    <td>
                                        <v-layout justify-center>
                                            {{obs}}
                                        </v-layout>
                                    </td>
                                </tr>
                            </tbody>
                        </template>
                    </v-simple-table>
                    <v-row>
                        <v-col>
                            <v-btn color="#2A3F54" dark depressed @click="onUpdate()">
                                <v-icon>mdi-file-pdf</v-icon> {{$t('perfil.vercur')}}
                            </v-btn>
                        </v-col>
                        <v-col>
                            <v-btn
                                color="#2A3F54"
                                dark
                                depressed
                                @click="onButtonClick('uploadercv');"
                            >
                                {{$t('perfil.atuacur')}}
                            </v-btn>
                        </v-col>
                    </v-row>
                    <input
                        ref="uploadercv"
                        class="d-none"
                        type="file"
                        accept="application/pdf"
                        @change="onFileChanged"
                    >
                </v-col>
            </v-row>
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
        </v-container>
    </div>
</template>
<script>
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import pdf from 'vue-pdf'
import navDrawLeitor from '../components/navDrawLeitor.vue'
import axios from 'axios'
export default {
    data(){
        return{
            ajuda:'perfil',
            username: this.$store.state.user._id,
            nome: this.$store.state.user.nome,
            email: this.$store.state.user.email,
            universidade: this.$store.state.user.universidade,
            departamento: this.$store.state.user.departamento,
            tipo: this.$store.state.user.tipo,
            data: this.$store.state.user.data,
            obs: this.$store.state.user.obs,
            userPic: '',
            //////////
            selectedFile: null,
            isSelecting: false,
            cv:'',
            cvDialog:false,
            pageCount:0,
            currentPage:0,
            page:1
        }
    },
    components:{
        'appHeader': Header,
        'navDrawLeitor':navDrawLeitor,
        'navDraw':NavDraw,
        'pdf':pdf
    },
    methods:{
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
            formData.append('curriculo',this.selectedFile)
            axios.post(`https://tommi2.di.uminho.pt/api/users/curriculo/atualizar/${this.username}`,formData,{
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
        onPicChanged(e) {
            this.selectedFile = e.target.files[0]
            let formData = new FormData()
            formData.append('foto',this.selectedFile)
            axios.post(`https://tommi2.di.uminho.pt/api/users/foto/atualizar/${this.username}`,formData,{
                responseType:'arraybuffer',
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`       
                }
                }).then(response => {
                    this.userPic=''
                    var image = new Buffer(response.data, 'binary').toString('base64')
                    this.userPic = `data:${response.headers['content-type'].toLowerCase()};base64,${image}`
                }).catch(e => {
                    this.errors.push(e)
                })
        },
        onUpdate(){
            axios.get(`https://tommi2.di.uminho.pt/api/users/curriculo/${this.username}?seed=${Date.now()}`, {
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
        this.userPic=''
        axios.get(`https://tommi2.di.uminho.pt/api/users/foto/${this.username}?seed=${Date.now()}`, {
            responseType:'arraybuffer',
            headers: {
                'Authorization': `Bearer: ${this.$store.state.jwt}`
            }
        })
        .then(response => {
            var image = new Buffer(response.data, 'binary').toString('base64')
            this.userPic = `data:${response.headers['content-type'].toLowerCase()};base64,${image}`
        }).catch(e => {
            this.errors.push(e)
        })
    }
}
</script>
<style scoped>
  #perfil *{
            box-sizing: border-box;
  }
  #perfil{
            margin: 20px auto;
            max-width: 800px;
  }
</style>
