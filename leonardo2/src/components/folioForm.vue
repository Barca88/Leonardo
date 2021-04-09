<template>
  <div id="registar">
      <v-card height="100%" width="100%">
        <v-toolbar color="#2A3F54" dark>
          <h1>{{$t('fol.title')}}</h1>
        </v-toolbar>
        <v-card-title>
          <h3>{{$t('folForm.visFol')}}</h3>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container>
                  <v-simple-table class="table">
                    <template v-slot:default>
                        <tbody>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.id')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{folio.idFolio}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.ver')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{folio.versao}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.tipo')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{folio.tipo}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.desc')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{folio.descricao}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.sum')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{folio.sumario}}
                                    </v-layout>
                                </td>
                            </tr>
                        </tbody>
                      </template>
                  </v-simple-table>
                  <p></p>
                  <v-dialog persistent v-model="dialog1" scrollable max-width="800px">
                    <template v-slot:activator="{ on }">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                            <v-btn v-on="{...on, ...tooltip}" class="mr-10 ml-5"><v-icon>mdi-text-box-search</v-icon></v-btn>
                        </template>
                        <span>
                            {{$t('folForm.tComTags')}}
                        </span>
                      </v-tooltip>
                    </template>
                    <v-card height="100%" width="100%">
                        <v-card-title>
                            <h1>{{$t('folForm.tComTags')}}</h1>
                            <div class="spacer"></div>
                            <v-btn @click="dialog1 = false" color="#c9302c" class="white--text">{{$t('indForm.close')}}</v-btn>
                        </v-card-title>
                        <v-card-text required>
                          {{this.folio.textoCTags}}         
                        </v-card-text>
                        <v-btn @click="dialog1 = false" color="#c9302c" class="white--text">{{$t('indForm.close')}}</v-btn>
                    </v-card>
                  </v-dialog>
                  <v-dialog persistent v-model="dialog2" scrollable max-width="800px" >
                      <template v-slot:activator="{ on }">
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on: tooltip }">
                              <v-btn v-on="{...on, ...tooltip}"><v-icon>mdi-text-box</v-icon></v-btn>
                          </template>
                          <span>
                              {{$t('folForm.tSemTags')}}
                          </span>
                        </v-tooltip>
                      </template>
                      <v-card height="100%" width="100%">
                          <v-card-title>
                              <h1>{{$t('folForm.tSemTags')}}</h1>
                              <div class="spacer"></div>
                              <v-btn @click="dialog2 = false" color="#c9302c" class="white--text">{{$t('indForm.close')}}</v-btn>
                          </v-card-title>
                          <v-card-text required>
                            {{this.folio.textoSTags}}         
                          </v-card-text>
                          <v-btn @click="dialog2 = false" color="#c9302c" class="white--text">{{$t('indForm.close')}}</v-btn>
                      </v-card>
                  </v-dialog>
              </v-container>
          </v-form>
          </v-card-actions>
          <v-toolbar flat>
            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <template v-slot:activator="{ on: tooltip }">
                  <v-btn @click="emiteFecho" v-on="{ ...tooltip}"><v-icon>mdi-exit-to-app</v-icon></v-btn>
              </template>
              <span>
                  {{$t('indForm.close')}}
              </span>
            </v-tooltip>
          </v-toolbar>
      </v-card>
  </div>
</template>

<script>
//import axios from 'axios'
//depois usar para estabelecer as rules dos campos do form
//import { required, email, max } from 'vee-validate/dist/rules'
//import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
// @ is an alias to /src

export default {
  data(){
    return{
      folio:{
        idFolio:"",
        versao:"",
        textoCTags:"",
        textoSTags:"",
        tipo:"",
        data:"",
        descricao:"",
        sumario:""
      },
      dialog1:false,
      dialog2:false
    }
  },
  props:{
    passedData:{
      type:Object
    }
  },
  methods: {
    /*post: function() {
      let formData = new FormData()
        formData.append('idFolio',this.folio.idFolio)
        formData.append('versao',this.folio.versao)
        formData.append('textoCTags',this.folio.textoCTags)
        formData.append('textoSTags',this.folio.textoSTags)
        formData.append('tipo',this.folio.tipo)
        formData.append('data',this.folio.data)
        formData.append('descricao',this.folio.descricao)
        formData.append('sumario',this.folio.sumario)
      
      if(this.value == 'editar'){
        axios.post(`http://localhost:5000/folios/editar/guardar?nome=` + this.folio.idFolio,formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`       
          }}
        )
        .then(response => {
            // JSON responses are automatically parsed.
            console.log(response.data)
            this.folios = response.data.folios
            this.atualizarInfo()
            //console.log('folioS: ' + this.folios[0].idFolio)
        }).catch(e => {
            console.log(e)
            this.errors.push(e)
        })
      }else if(this.value == 'adicionar'){
        axios.post('http://localhost:5000/folios/registar',formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`       
          }
        }).then(data => {
            console.log(data)
            this.folios = data.data.folios
            this.atualizarInfo()
        }) .catch(function (error) {
              console.log(error);
        });
      }
    },*/
    onUpdate(){
      this.folio.idFolio = this.passedData._id
      this.folio.versao = this.passedData.versao
      this.folio.textoCTags = this.passedData.textoCTags
      this.folio.textoSTags = this.passedData.textoSTags
      this.folio.tipo = this.passedData.tipo
      this.folio.data = this.passedData.data
      this.folio.descricao = this.passedData.descricao
      this.folio.sumario = this.passedData.sumario
    }/*,
    reset () {
      this.$refs.form.reset()
        this.folio.idFolio = "",
        this.folio.versao = "",
        this.folio.textoCTags = "",
        this.folio.textoSTags = "",
        this.folio.tipo = "",
        this.folio.data = "",
        this.folio.descricao = "",
        this.folio.sumario = ""
    }*/,
    atualizarInfo(){
      //console.log('ola')
      this.$emit('atualizarInfo')
    },
    emiteFecho(){
      this.$emit('emiteFecho')
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
  },
  created(){
    this.onUpdate()
  }/*
  created(){
    console.log('VALUE: ' + this.value)
    //console.log(this.passedData.email)
    if(this.value != 'adicionar'){
      this.folio.idFolio = this.passedData._id
      this.folio.versao = this.passedData.versao
      this.folio.textoCTags = this.passedData.textoCTags
      this.folio.textoSTags = this.passedData.textoSTags
      this.folio.tipo = this.passedData.tipo
      this.folio.data = this.passedData.data
      this.folio.descricao = this.passedData.descricao
      this.folio.sumario = this.passedData.sumario
    }
  },
  updated(){
    if(this.folio.idFolio && this.folio.versao && this.folio.textoCTags && this.folio.textoSTags && this.folio.tipo && this.folio.descricao && this.folio.sumario){
      this.$refs.submit.disabled = false
    }
    console.log("data updated")
  }*/
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
