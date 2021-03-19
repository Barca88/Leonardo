<template>
    <div id="import">
        <appHeader :ajuda='ajuda'></appHeader>
        <navDraw></navDraw>
        <v-sheet
            class="mx-auto"
            elevation="8"
            max-width="800"
        >   
            <div class="import">
                <v-progress-linear
                :size="100"
                :value="value"
                :height="30"
                color="primary"
                >
                    {{value}}%
                </v-progress-linear>
            </div>
            <v-card>
                <v-window v-model="model">
                    <v-window-item
                    v-for="n in 6"
                    :key="n"
                    >
                        <v-toolbar dark flat color="#2A3F54">
                            <h3 class="ml-5"> {{$t('imp.passo')}}</h3>
                            <h3 v-if="n==1">/{{$t('p1.ins')}}</h3>
                            <h3 v-else-if="n==2">/{{$t('p2.tit')}}</h3>
                            <h3 v-else-if="n==3">/{{$t('p3.av')}}</h3>
                            <h3 v-else-if="n==4">/{{$t('p4.tit')}}</h3>
                            <h3 v-else-if="n==5">/{{$t('p5.tit')}}</h3>
                            <h3 v-else-if="n==6">/{{$t('p6.tit')}}</h3>
                            <v-spacer/>
                            <h3 class="mr-5">{{"(" + n + "/6)"}}</h3>
                        </v-toolbar>
                        <passo1 v-if="n == 1 && renderComponent" :folio="info" :cancelado="cancelado" @atualizaFolio=atualizaFolio($event)></passo1>
                        
                        <passo2 v-else-if="n == 2" :folio="info" @cancela=cancela()></passo2>
                        
                        <passo3 v-else-if="n == 3 && renderComponent" :folio="info" @cancela=cancela()></passo3>
                        
                        <passo4 v-else-if="n == 4 && renderComponent" :folio="info" @cancela=cancela()></passo4>
                        
                        <passo5 v-else-if="n == 5 && renderComponent" :folio="info" @cancela=cancela()></passo5>
                        
                        <passo6 v-else-if="n == 6 && renderComponent" :folio="info" :fileInfo="passo6info" @submeterFolio=submeterFolio() @cancela=cancela()></passo6>

                        <v-toolbar flat color="white" v-if="n!=1 && n!=6">
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on: tooltip }">
                                    <v-btn @click="prev" v-on="{ ...tooltip}" class="mr-5"><v-icon>mdi-arrow-left</v-icon></v-btn>
                                </template>
                                <span>
                                    {{$t('imp.back')}}
                                </span>
                            </v-tooltip>
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on: tooltip }">
                                    <v-btn ref="submit" color="#26B99A" class="white--text mr-5" @click="next();" v-on="{ ...tooltip}"><v-icon>mdi-check</v-icon></v-btn>
                                </template>
                                <span>
                                    {{$t('p1.sub')}}
                                </span>
                            </v-tooltip>
                        </v-toolbar>
                        <v-dialog
                            v-model="fotoErro"
                            scrollable 
                            width="500"
                            persistent
                        >
                            <v-card>
                                <v-toolbar color="#2A3F54" dark>
                                    <h2>{{$t('reg.pag')}}</h2>
                                </v-toolbar>
                                <v-row>
                                <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                                    <v-icon x-large color="#c9302c" dark>mdi-close</v-icon>
                                </v-col>
                                <v-col>
                                    <v-card-text>
                                        <h3>{{$t('imp.seq')}}</h3>
                                    </v-card-text>
                                </v-col>
                                </v-row>

                                <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on: tooltip }">
                                    <v-btn @click="fotoErro = false" v-on="{ ...tooltip}">
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
                    </v-window-item>
                </v-window>
                
            </v-card>
        </v-sheet>
        <v-dialog @keydown.esc="failureDialog = false" v-model="failureDialog" scrollable width="500"> 
            <v-card>
                <v-toolbar color="#2A3F54" dark>
                <h2>{{$t('reg.pag')}}</h2>
                </v-toolbar>
                <v-divider
                class="mx-4"
                horizontal
            ></v-divider>

                <v-row>
                <v-col style="margin-left:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="#c9302c" dark>mdi-close</v-icon>
                </v-col>
                <v-col>
                    <v-card-text class="mt-2">
                        {{$t('imp.new')}}
                    </v-card-text>
                </v-col>
                </v-row>
                <v-card-actions>
                <v-spacer></v-spacer>
                
                <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="failureDialog=false" v-on="on">
                        <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                    </template>
                    <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
    import Header from '../components/header.vue'
    import NavDraw from '../components/navDraw.vue'
    import Passo1 from '../components/passo1.vue'
    import Passo2 from '../components/passo2.vue'
    import Passo3 from '../components/passo3.vue'
    import Passo4 from '../components/passo4.vue'
    import Passo5 from '../components/passo5.vue'
    import Passo6 from '../components/passo6.vue'
    import axios from 'axios'
    export default {
        data: () => ({
            value: null,
            model: null,
            ajuda:'imports',
            info:{
                idFolio:"",
                versao:"",
                tipo:"",
                descricao:"",
                obs:"",
                sumario:"",
                textoTags:"",
                textoSTags:"",
                tags:[],
                list:[],
                foto:null,
                ficheiro:null,
            },
            passo6info: {},
            cancelado: 0,
            renderComponent: true,
            fotoErro:false,
            failureDialog:false
        }),
        components:{
            'appHeader': Header,
            'navDraw':NavDraw,
            'passo1':Passo1,
            'passo2':Passo2,
            'passo3':Passo3,
            'passo4':Passo4,
            'passo5':Passo5,
            'passo6':Passo6
        },
        methods:{
            prev(){
                this.model -= 1
            },
            next(){
                this.model += 1
            },
            cancela(){
                this.info.idFolio=""
                this.info.versao=""
                this.info.tipo=""
                this.info.descricao=""
                this.info.obs=""
                this.info.sumario=""
                this.info.foto=null
                this.info.ficheiro=null
                this.info.textoTags=""
                this.info.textoSTags=""                
                this.info.tags=[]
                this.info.list=[]
                this.passo6info={}
                //console.log('Info:' + JSON.stringify(this.info))
                this.model = 0
                this.renderComponent = false;
                this.$nextTick (() => {
                    // add my-component component in DOM
                    this.renderComponent = true;
                });
            },
            atualizaFolio(folio){
                //console.log(folio)
                this.info.idFolio=folio.idFolio
                this.info.versao=folio.versao
                this.info.tipo=folio.tipo
                this.info.descricao=folio.descricao
                this.info.obs=folio.obs
                this.info.sumario=folio.sumario
                this.info.foto=folio.foto
                this.info.ficheiro=folio.ficheiro

                //console.log('FILE1: ' + this.info.ficheiro)

                let formData = new FormData()
                formData.append('idFolio',this.info.idFolio)
                formData.append('versao',this.info.versao)
                formData.append('tipo',this.info.tipo)
                formData.append('obs',this.info.obs)
                formData.append('descricao',this.info.descricao)
                formData.append('sumario',this.info.sumario)
                formData.append('foto',this.info.foto)
                formData.append('ficheiro',this.info.ficheiro)
            
                // axios.post(`https://tommi2.di.uminho.pt/api/import/passo1/?nome=${this.$store.state.user._id}`,formData,{
                axios.post(`https://tommi2.di.uminho.pt/api/import/passo1/?nome=${this.$store.state.user._id}`,formData,{
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`       
                }
                }).then(data => {
                    //console.log(data)
                    //if folio ok 
                    if( data.data.message == 'não existe'){
                        //console.log("O FOLIO NÂO EXISTE")
                        //passos 2, 4, e 5?
                        this.info.textoTags=data.data.textoTags
                        this.info.textoSTags=data.data.textoSTags
                        this.info.tags=data.data.tags
                        this.info.list=data.data.list
                        this.passo6info=data.data.passo6
                        if(folio.skip == 1){
                            this.model = 5
                        }else{
                            this.next()
                        }
                    }
                    //folio not ok
                    else {
                        this.failureDialog = true
                    }
                }) .catch(() => {
                    this.fotoErro = true
                    //console.log(e)
                    //this.errors.push(e)
                })

            },
            submeterFolio(){
                let formData = new FormData()
                formData.append('idFolio',this.info.idFolio)
                formData.append('versao',this.info.versao)
                formData.append('tipo',this.info.tipo)
                formData.append('obs',this.info.obs)
                formData.append('descricao',this.info.descricao)
                formData.append('sumario',this.info.sumario)
                formData.append('foto',this.info.foto)
                formData.append('ficheiro',this.info.ficheiro)
                formData.append('textoTags',this.info.textoTags)
                formData.append('textoSTags',this.info.textoSTags)
                //console.log(this.info.list)
                axios.post(`https://tommi2.di.uminho.pt/api/import/passo6/?nome=${this.$store.state.user._id}`,formData,{headers:{
                    'Content-Type': 'multipart/form-data',
                    Authorization:`Bearer: ${this.$store.state.jwt}`
                }})
                .then(() => {
                    // JSON responses are automatically parsed.
                    //console.log(response.data)
                    this.model=0
                    //this.infos[0] = response.data.info
                    //console.log(this.infos)
                }).catch(e => {
                    this.errors.push(e)
                })
                this.cancela()
            }
        },
        updated () {
            if(this.model == null){
                this.value = 0
            }
            this.value = parseInt(100/6 * this.model,10)
        }
    }
</script>

<style scoped>
    #import{
        margin-bottom: 50px;
    }
.mx-auto .import{
            margin: 20px auto;
            max-width: 800px;
  }
</style>