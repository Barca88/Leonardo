<template>
  <div id="registar">
    <v-toolbar color="#2A3F54" dark>
      <h1>{{$t('navd.docum')}}</h1>
    </v-toolbar>
      <v-card height="100%" >
        <v-card-title>
          <h3>{{$t('docs.ins')}}</h3>
        </v-card-title>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container class="ml-5">
                <div style="width:80%">
                    <v-text-field
                          :label="$t('docs.id')"
                          v-model="doc.titulo"
                          :rules="[rules.required]"      
                    ></v-text-field>
                  <v-row>
                    <v-text-field
                        :label="$t('docs.aut')"
                        :rules="[rules.required]"
                        v-model="doc.autores"
                    ></v-text-field>
                    <h5 style="color:red">*</h5>
                  </v-row>
                  <v-row>
                    <v-text-field
                        :label="$t('docForm.descL')"
                        :rules="[rules.required]"
                        v-model="doc.desc"
                    ></v-text-field>
                    <h5 style="color:red">*</h5>
                  </v-row>
                  <v-container fluid>
                  <v-radio-group v-model="doc.tipo" column>
                      <v-radio :label="$t('docForm.art')" value="Artigo"></v-radio>
                      <v-radio :label="$t('docForm.man')" value="Manual"></v-radio>
                      <v-radio :label="$t('docForm.rel')" value="Relatório Técnico"></v-radio>
                      <v-radio :label="$t('docForm.diss')" value="Dissertação"></v-radio>
                  </v-radio-group>
                  </v-container>
                  <v-row>
                    <v-text-field
                        :label="$t('docs.data')"
                        :rules="[rules.required]"
                        v-model="doc.data"
                    ></v-text-field>
                    <h5 style="color:red">*</h5>
                  </v-row>
                  <v-row align="center">
                      <label>{{$t('docForm.file')}}:</label>
                      <v-file-input show-size type="file" :label="$t('p1.file')" v-model="doc.ficheiro"></v-file-input>
                      <h5 style="color:red">*</h5>
                  </v-row>
                </div>
              </v-container>
              <v-container>
                <div style="width:90%">
                  <v-row>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on: tooltip }" >
                          <v-btn @click.prevent="reset" v-on="{ ...tooltip}" class="ml-12 mr-5"><v-icon>mdi-history</v-icon></v-btn>
                      </template>
                      <span>
                          {{$t('p1.reset')}}
                      </span>
                    </v-tooltip>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on: tooltip }">
                          <v-btn ref="submit" @click="post()" class="mr-5" :disabled="disableButton" v-on="{ ...tooltip}"><v-icon>mdi-check</v-icon></v-btn>
                      </template>
                      <span>
                          {{$t('docs.conf')}}
                      </span>
                    </v-tooltip>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on: tooltip }">
                          <v-btn @click="dialogHelp=true" v-on="{ ...tooltip}" class="mr-5"><v-icon>mdi-help</v-icon></v-btn>
                      </template>
                      <span>
                          {{$t('p1.ajuda')}}
                      </span>
                    </v-tooltip>
                    <v-dialog @keydown.esc="dialogHelp = false"  v-model="dialogHelp" scrollable width="500">
                      <v-card>
                        <v-toolbar color="#2A3F54" dark>
                            <h2>{{$t('navd.docum')}}</h2>
                        </v-toolbar>
                        <v-row>
                        <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                            <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                        </v-col>
                        <v-col>
                            <v-card-text>
                            <h3>{{$t('docForm.help')}}</h3>
                            </v-card-text>
                        </v-col>
                        </v-row>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          
                          <v-tooltip bottom> 
                            <template v-slot:activator="{ on }">
                                <v-btn depressed color="white" @click="dialogHelp=false" v-on="on">
                                  <v-icon large>mdi-exit-to-app</v-icon>
                                </v-btn>
                              </template>
                              <span>{{ $t('nav.Sair') }}</span>
                            </v-tooltip>

                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                    <v-spacer></v-spacer>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on: tooltip }">
                          <v-btn @click="emiteFecho" v-on="{ ...tooltip}"><v-icon>mdi-exit-to-app</v-icon></v-btn>
                      </template>
                      <span>
                          {{$t('indForm.close')}}
                      </span>
                    </v-tooltip>
                  </v-row>
                </div>
              </v-container>
          </v-form>
      </v-card>
      <v-dialog @keydown.esc="failureDialog = false" v-model="failureDialog" scrollable width="500"> 
        <v-card>
          <v-toolbar color="#2A3F54" dark>
            <h2>{{$t('navd.docum')}}</h2>
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
                {{$t('uF.badChoice')}}
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
import axios from 'axios'
//depois usar para estabelecer as rules dos campos do form
//import { required, email, max } from 'vee-validate/dist/rules'
//import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
// @ is an alias to /src

export default {
  data(){
    return{
      doc:{
        titulo:"",
        desc:"",
        autores:"",
        data:"",
        tipo:"",
        ficheiro:{},
      },
      dialog:false,
      dialogHelp:false,
      valid:true,
      failureDialog:false,
      rules: {
          required: value => !!value || 'Required.',
      }
    }
  },
  props:{
    passedData:{
      type:Object
    },
    value:{
      type:String
    }
  },
  watch:{
    passedData: {
        immediate: true,
        deep: true,
        handler(){
            this.onUpdate()
        }
    }
  },methods:{
    onUpdate(){
        this.doc.titulo = ''
        this.doc.desc = ''
        this.doc.autores = ''
        this.doc.data = ''
        this.doc.tipo = ''
    },
    post: function() {
      let formData = new FormData()
        formData.append('titulo',this.doc.titulo)
        formData.append('desc',this.doc.desc)
        formData.append('autores',this.doc.autores)
        formData.append('data',this.doc.data)
        formData.append('tipo',this.doc.tipo)
        formData.append('ficheiro',this.doc.ficheiro)

        axios.post('https://tommi2.di.uminho.pt/api/documentacao/adicionar',formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`       
          }
        }).then(data => {
            if(data.data.message){
              this.failureDialog = true
            }
            else{
              //this.users = data.data.docs
              this.$refs.form.reset()
              this.atualizarInfo()
            }
        }).catch(e => {
            this.errors.push(e)
        })
    },
    reset () {
      this.$refs.form.reset()
      this.doc.titulo=''
      this.doc.desc=''
      this.doc.autores=''
      this.doc.data=''
      this.doc.tipo = ''
      this.doc.ficheiro={}
    },
    atualizarInfo(){
      //console.log('ola')
      this.$emit('atualizarInfo')
    },
    emiteFecho(){
      this.$emit('emiteFecho')
    }
  },
  created(){
    this.onUpdate()
  },
  computed:{
    disableButton (){
      if (this.valid && this.doc.titulo.length > 0 && this.doc.autores.length > 0 && this.doc.desc.length > 0 && this.doc.data.length > 0 && this.doc.ficheiro && this.doc.tipo)
        return false
      else
        return true
    } 
  },
}
</script>
<style scoped>
  #registar *{
            box-sizing: border-box;
  }
  #registar{
            margin: 20px auto;
            max-width: 800px;
  }
  #checkboxes input{
            display: inline-block;
            margin-right: 10px;
  }
  #checkboxes label{
            display: inline-block;
  }
</style>
