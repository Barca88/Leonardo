<template>
  <div id="registar">
    <v-toolbar color="#2A3F54" dark>
      <h1>{{$t('navd.docum')}}</h1>
    </v-toolbar>
    <v-card v-if= "value === 'ver'">
        <v-card-title>
          <h3>{{$t('docs.ver')}}</h3>
        </v-card-title>
        <v-container>
          <v-simple-table class="table mr-10 ml-10">
            <template v-slot:default>
                <tbody>
                    <tr>
                        <td class="text-left"><b>{{$t('docs.id')}}</b></td>
                        <td>
                            <v-layout>
                                {{doc.titulo}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('docs.aut')}}</b></td>
                        <td>
                            <v-layout>
                                {{doc.authors}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('docForm.descL')}}</b></td>
                        <td>
                            <v-layout>
                                {{doc.desc}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('docs.tipo')}}</b></td>
                        <td>
                            <v-layout>
                                {{doc.type}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('docs.data')}}</b></td>
                        <td>
                            <v-layout>
                                {{doc.date}}
                            </v-layout>
                        </td>
                    </tr>
                </tbody>
            </template>
          </v-simple-table>
          <v-row>
            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <template v-slot:activator="{ on: tooltip }">
                  <v-btn @click="dialogHelp=true" v-on="{ ...tooltip}" class="mr-5"><v-icon>mdi-help</v-icon></v-btn>
              </template>
              <span>
                  {{$t('p1.ajuda')}}
              </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on: tooltip }">
                  <v-btn @click="emiteFecho" v-on="{ ...tooltip}" class="mr-10"><v-icon>mdi-exit-to-app</v-icon></v-btn>
              </template>
              <span>
                  {{$t('indForm.close')}}
              </span>
            </v-tooltip>
          </v-row>
        </v-container>
      </v-card>
      <v-card v-else height="100%">
        <v-card-title v-if= "value === 'adicionar'">
          <h3>{{$t('docs.ins')}}</h3>
        </v-card-title>
        <v-card-title v-else>
          <h3>{{$t('docs.editar')}}</h3>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container class="ml-5">
                 <v-row>
                    <v-col cols="12" sm="16" md="4">
                      <v-text-field 
                          v-if= "value === 'adicionar'"
                          :label="$t('docs.id')"
                          v-model="doc.titulo"
                          :rules="[rules.required,...rules.repeatedID]"            
                      ></v-text-field>
                      <v-text-field 
                          v-else-if="value === 'editar'"
                          :label="$t('docs.id')"
                          v-model="doc.titulo"
                          :rules="[rules.required]"
                          disabled
                      ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="16" md="4">
                      <v-text-field
                          v-if= "value != 'ver'"
                          :label="$t('docs.aut')"
                          v-model="doc.authors"
                          :rules="[rules.required]"  
                      ></v-text-field>
                  </v-col>
                  <v-col>
                    <v-text-field
                      v-if= "value != 'ver'"
                      :label="$t('docForm.descL')"
                      v-model="doc.desc"
                      :rules="[rules.required, rules.email]"
                      required
                  ></v-text-field>
                  </v-col>
                 </v-row>
                   <v-container fluid>
                  <v-radio-group v-model="doc.type" :label="$t('nav.tipoDeTexto')" column>
                      <v-radio :label="$t('docForm.art')" value="Artigo"></v-radio>
                      <v-radio :label="$t('docForm.man')" value="Manual"></v-radio>
                      <v-radio :label="$t('docForm.rel')" value="Relatório Técnico"></v-radio>
                      <v-radio :label="$t('docForm.diss')" value="Dissertação"></v-radio>
                  </v-radio-group>
                  </v-container>
                  <v-text-field
                      v-if= "value != 'ver'"
                      :label="$t('docs.data')"
                      :rules="[rules.required]"
                      v-model="doc.date"
                  ></v-text-field>
                  <v-row align="center" v-if= "value === 'adicionar' || value ==='editar'">
                      <label>{{$t('docForm.file')}}:</label>
                      <v-file-input show-size v-model="doc.ficheiro"></v-file-input>
                  </v-row>
                  <br>
                  <v-row>
                    <v-tooltip bottom v-if= "value === 'adicionar' || value === 'editar'">
                      <template v-slot:activator="{ on: tooltip }" >
                          <v-btn @click.prevent="reset" v-on="{ ...tooltip}" class="ml-12 mr-5"><v-icon>mdi-history</v-icon></v-btn>
                      </template>
                      <span>
                          {{$t('p1.reset')}}
                      </span>
                    </v-tooltip>
                    <v-tooltip bottom v-if= "value === 'adicionar' || value === 'editar'">
                      <template v-slot:activator="{ on: tooltip }">
                          <v-btn ref="submit" @click="post()" :disabled="disableButton" v-on="{ ...tooltip}"><v-icon>mdi-check</v-icon></v-btn>
                      </template>
                      <span>
                          {{$t('uF.conf')}}
                      </span>
                    </v-tooltip>
                    <v-spacer></v-spacer>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on: tooltip }">
                          <v-btn @click="dialogHelp=true" v-on="{ ...tooltip}" class="mr-5"><v-icon>mdi-help</v-icon></v-btn>
                      </template>
                      <span>
                          {{$t('p1.ajuda')}}
                      </span>
                    </v-tooltip>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on: tooltip }">
                          <v-btn @click="emiteFecho" v-on="{ ...tooltip}"><v-icon>mdi-exit-to-app</v-icon></v-btn>
                      </template>
                      <span>
                          {{$t('indForm.close')}}
                      </span>
                    </v-tooltip>
                  </v-row>
              </v-container>
          </v-form>
          </v-card-actions>
      </v-card>
      <v-dialog @keydown.esc="dialogHelp = false"  v-model="dialogHelp" scrollable width="500">
          <v-card>
            <v-toolbar color="#2A3F54" dark>
                <h2>{{$t('adminNav.doc')}}</h2>
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
        authors:"",
        date:"",
        type:"",
        ficheiro:{},
      },
      dialog:false,
      dialogHelp:false,
      valid:true,
      failureDialog:false,
      idDocs: [],
      rules: {
          required: value => !!value || 'Required.',
          repeatedID: [v => this.checkID(v) || "ID already exists"],
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
      if(this.value != 'adicionar'){
        console.log(this.passedData)
        this.doc.titulo = this.passedData._id
        this.doc.desc = this.passedData.desc
        this.doc.authors = this.passedData.authors
        this.doc.date = this.passedData.date
        this.doc.type = this.passedData.type
      }
      else{
        this.doc.titulo = ''
        this.doc.desc = ''
        this.doc.authors = ''
        this.doc.date = ''
        this.doc.type = ''
      }
    },
    post: function() {
      let formData = new FormData()
        formData.append('titulo',this.doc.titulo)
        formData.append('desc',this.doc.desc)
        formData.append('autores',this.doc.authors)
        formData.append('data',this.doc.date)
        formData.append('tipo',this.doc.type)
        formData.append('ficheiro',this.doc.ficheiro)

      if(this.value == 'adicionar'){
        axios.post(`${process.env.VUE_APP_BACKEND}/documentacao/adicionar?nome=${this.$store.state.user._id}`,formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"       
          }
        }).then(data => {
            if(data.data.message){
              this.failureDialog = true
            }
            else{
              this.docs = data.data.docs
              this.$refs.form.reset()
              this.atualizarInfo()
            }
        }).catch(e => {
            this.errors.push(e)
        })
      }else if(this.value == 'editar'){
        axios.post(`${process.env.VUE_APP_BACKEND}/documentacao/editar?nome=${this.$store.state.user._id}`,formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"       
          }
        }).then(data => {
          console.log(data.data)
            this.docs = data.data.docs
            this.$refs.form.reset()
            this.atualizarInfo()
        }).catch(e => {
            this.errors.push(e)
        })
      }
    },
    reset () {
      if(this.value == 'adicionar'){
        this.doc.titulo=''
      }
      this.doc.desc=''
      this.doc.authors=''
      this.doc.date=''
      this.doc.type = ''
      this.doc.ficheiro={}
    },
    atualizarInfo(){
      //console.log('ola')
      this.$emit('atualizarInfo')
    },
    emiteFecho(){
      this.$emit('emiteFecho')
    },
    checkID(item){
      return !this.idDocs.find(x => x === item)
    },
  },
  created(){
    axios.get(`${process.env.VUE_APP_BACKEND}/documentacao/docs`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
    .then(response => {
        response.data.docs.forEach((obj) =>{
          this.idDocs.push(obj._id)
        });
    }).catch(e => {
        //console.log(e)
        this.errors.push(e)
    })
    this.onUpdate()
  },
  computed:{
    disableButton (){
      if (this.valid && this.doc.titulo.length > 0 && this.doc.authors.length > 0 && this.doc.desc.length > 0 && this.doc.date.length > 0 && this.doc.ficheiro && this.doc.type)
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
