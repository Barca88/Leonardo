<template>
    <div id="resumo">
        <v-sheet
        color="white"
        tile
        >
            <v-data-table
                :headers="headers"
                :items="infos"
                :sort-by="['idFolio','descricao','tipo','n_folios','n_linhas','n_tags','n_indices']"
                :sort-desc="[true,false,true,true,true,true,true]"
                multi-sort            
            >
            </v-data-table>
            <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                    <v-btn @click.prevent="reset" v-on="{ ...tooltip}" class="ml-5 mb-5"><v-icon>mdi-history</v-icon></v-btn>
                </template>
                <span>
                    {{$t('p1.reset')}}
                </span>
            </v-tooltip>
            <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                    <v-btn ref="submit" color="#26B99A" class="white--text ml-5 mb-5" @click="successDialog = true" v-on="{ ...tooltip}"><v-icon>mdi-check</v-icon></v-btn>
                </template>
                <span>
                    {{$t('p1.sub')}}
                </span>
            </v-tooltip>
            <v-dialog v-model="successDialog" scrollable width="500" persistent>
                <v-card>
                    <v-toolbar color="#2A3F54" dark>
                        <h2>{{$t('reg.pag')}}</h2>
                    </v-toolbar>
                    <v-row>
                        <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                        <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
                        </v-col>
                        <v-col>
                        <v-card-text>
                            <h3>{{$t('p6.sucD')}}</h3>
                        </v-card-text>
                        </v-col>
                    </v-row>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                            <v-btn @click="successDialog = false;save();" v-on="{ ...tooltip}">
                            <v-icon>mdi-exit-to-app</v-icon>
                            </v-btn>
                        </template>
                        <span>
                            {{$t('navd.close')}}
                        </span>
                        </v-tooltip>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-sheet>
    </div>
</template>
<script>
//import axios from 'axios'
export default {
    data(){
        return{
            headers:[
                {
                    text: `${this.$t('p1.id')}`,
                    align: 'start',
                    value: 'idFolio'
                },
                {
                    text:`${this.$t('p1.desc')}`,
                    value: 'descricao'
                },
                {
                    text:`${this.$t('p1.tipo')}`,
                    value: 'tipo'
                },
                {
                    text:`${this.$t('p6.nfolios')}`,
                    value: 'n_folios'
                },
                {
                    text:`${this.$t('p6.nlinhas')}`,
                    value: 'n_linhas'
                },
                {
                    text:`${this.$t('p6.ntags')}`,
                    value: 'n_tags'
                },
                {
                    text:`${this.$t('p6.nindices')}`,
                    value: 'n_indices'
                }
            ],
            infos:[],
            errors:[],
            successDialog:false
        }
    },
    props:{
        folio:{
            type:Object
        },
        fileInfo:{
            type:Object
        }
    },
    watch:{
        folio: {
            immediate: true,
            deep: true,
            handler(){
                this.onUpdateFolio()
            }
        }
    },
    methods:{
        onUpdateFolio(){
            var obj = {}
            obj.idFolio = this.folio.idFolio
            obj.descricao = this.folio.descricao
            obj.tipo = this.folio.tipo
            obj.n_folios = this.fileInfo.n_folios
            obj.n_tags = this.fileInfo.n_tags
            obj.n_indices = this.fileInfo.n_indices
            obj.n_linhas = this.fileInfo.n_linhas
            this.infos = [obj]
        },
        save (){
            this.$emit('submeterFolio', this)
        },
        reset(){
            this.$emit('cancela')
        }
    },
    created() {
        this.onUpdateFolio()
    }
}
</script>
<style scoped>
    #resumo *{
            box-sizing: border-box;
    }
    #resumo{
            margin: 20px auto;
            max-width: 800px;
    }
</style>