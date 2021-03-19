<template>
  <div id="registar">
    <v-toolbar color="#2A3F54" dark>
      <h1>{{$t('navd.tags')}}</h1>
    </v-toolbar>
    <v-card v-if= "value === 'ver'">
      <v-card-title>
        <h3>{{$t('defForm.visDef')}}</h3>
      </v-card-title>
      <v-simple-table class="table">
        <template v-slot:default>
            <tbody>
                <tr>
                    <td class="text-left"><b>{{$t('defForm.elem')}}</b></td>
                    <td>
                        <v-layout class="ml-12">
                            {{definition.elemento}}
                        </v-layout>
                    </td>
                </tr>
                <tr>
                    <td class="text-left"><b>{{$t('defForm.desc')}}</b></td>
                    <td>
                        <v-layout class="ml-12">
                            {{definition.desc}}
                        </v-layout>
                    </td>
                </tr>
                <tr>
                    <td class="text-left"><b>{{$t('defForm.wac')}}</b></td>
                    <td>
                        <v-layout class="ml-12">
                            {{definition.wac}}
                        </v-layout>
                    </td>
                </tr>
                <tr>
                    <td class="text-left"><b>{{$t('defForm.tag')}}</b></td>
                    <td>
                        <v-layout class="ml-12">
                            {{definition.tag}}
                        </v-layout>
                    </td>
                </tr>
                <tr>
                    <td class="text-left"><b>{{$t('defForm.ex')}}</b></td>
                    <td>
                        <v-layout class="ml-12">
                            {{definition.exemplo}}
                        </v-layout>
                    </td>
                </tr>
                <tr>
                    <td class="text-left"><b>{{$t('defForm.pro')}}</b></td>
                    <td>
                        <v-layout class="ml-12">
                            {{definition.procurar}}
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
              <v-btn @click="dialogHelp=true" v-on="{ ...tooltip}" class="mr-5 mb-5"><v-icon>mdi-help</v-icon></v-btn>
          </template>
          <span>
              {{$t('p1.ajuda')}}
          </span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on: tooltip }">
              <v-btn class="mr-12 mb-5" @click="emiteFecho" v-on="{ ...tooltip}"><v-icon>mdi-exit-to-app</v-icon></v-btn>
          </template>
          <span>
              {{$t('indForm.close')}}
          </span>
        </v-tooltip>
      </v-row>
    </v-card>
      <v-card v-else height="100%" width="100%">
        <v-card-title v-if= "value === 'adicionar'">
          <h3>{{$t('defForm.addDef')}}</h3>
        </v-card-title>
        <v-card-title v-else>
          <h3>{{$t('defForm.edDef')}}</h3>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container>
                  <v-text-field v-if="value != 'ver'"
                      :label="$t('defForm.elem')"
                      v-model="definition.elemento"
                      required
                  ></v-text-field>
                  <v-text-field v-if="value != 'ver'"
                      :label="$t('defForm.desc')"
                      v-model="definition.desc"
                      required   
                  ></v-text-field>
                  <v-text-field v-if="value != 'ver'"
                      :label="$t('defForm.wac')"
                      v-model="definition.wac"
                      required            
                  ></v-text-field>
                  <v-text-field v-if="value != 'ver'"
                      :label="$t('defForm.tag')"
                      v-model="definition.tag"
                  ></v-text-field>
                  <v-text-field v-if="value != 'ver'"
                      :label="$t('defForm.ex')"
                      v-model="definition.exemplo"
                  ></v-text-field>
                  <v-container fluid v-if="value != 'ver'">
                  <label>{{$t('defForm.pro')}}</label>
                  <v-radio-group  v-model="definition.procurar" column>
                      <v-radio :label="$t('defForm.sim')" value="sim"></v-radio>
                      <v-radio :label="$t('defForm.nao')" value="nao"></v-radio>
                  </v-radio-group>
                  </v-container>
                  <br>
              </v-container>
          </v-form>
          </v-card-actions>
        <v-row>
          <v-tooltip bottom v-if="value === 'adicionar' || value === 'editar'">
            <template v-slot:activator="{ on: tooltip }">
                <v-btn @click.prevent="reset" v-on="{ ...tooltip}" class="ml-12 mr-5 mb-5"><v-icon>mdi-history</v-icon></v-btn>
            </template>
            <span>
                {{$t('p1.reset')}}
            </span>
          </v-tooltip>
          <v-tooltip bottom v-if="value === 'adicionar' || value === 'editar'">
            <template v-slot:activator="{ on: tooltip }">
                <v-btn ref="submit" @click="post()" class="mb-5" v-bind:class="{disabled: disableButton}" :disabled="disableButton" v-on="{ ...tooltip}"><v-icon>mdi-check</v-icon></v-btn>
            </template>
            <span>
                {{$t('uF.conf')}}
            </span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
                <v-btn @click="dialogHelp=true" v-on="{ ...tooltip}" class="mr-5 mb-5"><v-icon>mdi-help</v-icon></v-btn>
            </template>
            <span>
                {{$t('p1.ajuda')}}
            </span>
          </v-tooltip>
          <v-dialog @keydown.esc="dialogHelp = false"  v-model="dialogHelp" scrollable width="500">
            <v-card>
              <v-toolbar color="#2A3F54" dark>
                  <h2>{{$t('navd.tags')}}</h2>
              </v-toolbar>
              <v-row>
              <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                  <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
              </v-col>
              <v-col>
                  <v-card-text>
                  <h3>{{$t('def.help')}}</h3>
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
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
                <v-btn class="mr-12 mb-5" @click="emiteFecho" v-on="{ ...tooltip}"><v-icon>mdi-exit-to-app</v-icon></v-btn>
            </template>
            <span>
                {{$t('indForm.close')}}
            </span>
          </v-tooltip>
        </v-row>
      </v-card>
  </div>
</template>


<script>
import axios from 'axios'
//depois usar para estabelecer as rules dos campos do form
//import { required, wac, max } from 'vee-validate/dist/rules'
//import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
// @ is an alias to /src

export default {
  data(){
    return{
      definition:{
        elemento:"",
        desc:"",
        wac:"",
        tag:"",
        exemplo:"",
        procurar:""
      },
      dialogHelp:false,
      dialog:false
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
      //console.log(typeof this.value)
      //console.log('VALUE: ' + this.value)
      //console.log('procura: ' + this.passedData.procura)
      if(this.value != 'adicionar'){
        this.definition.elemento = this.passedData._id
        this.definition.desc = this.passedData.desc
        this.definition.wac = this.passedData.wac
        this.definition.tag = this.passedData.tag
        this.definition.exemplo = this.passedData.exemplo
        if(this.passedData.procura == false){
            this.definition.procurar = 'nao'
        }else{
            this.definition.procurar = 'sim'
        }
      }
      else{
        this.definition.elemento = ''
        this.definition.desc = ''
        this.definition.wac = ''
        this.definition.tag = ''
        this.definition.exemplo = ''
        this.definition.procurar = ''
      }
    },
    post: function() {
      let formData = new FormData()
        formData.append('elemento',this.definition.elemento)
        formData.append('desc',this.definition.desc)
        formData.append('wac',this.definition.wac)
        formData.append('tag',this.definition.tag)
        formData.append('exemplo',this.definition.exemplo)
        formData.append('procurarr',this.definition.procurar)
      
      if(this.value == 'editar'){
        axios.post(`https://tommi2.di.uminho.pt/api/settings/editar/guardar?desc=` + this.definition.elemento,formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`       
          }}
        )
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            this.settings = response.data.settings
            this.$refs.form.reset()
            this.atualizarInfo()
            //console.log('USERS: ' + this.users[0].elemento)
        }).catch(e => {
            //console.log(e)
            this.errors.push(e)
        })
      }else if(this.value == 'adicionar'){
        axios.post('https://tommi2.di.uminho.pt/api/settings/registar',formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`       
          }
        }).then(data => {
            //console.log(data)
            this.settings = data.data.settings
            this.$refs.form.reset()
            this.atualizarInfo()
        }).catch(e => {
            this.errors.push(e)
        })
      }
    },
    reset () {
      this.$refs.form.reset()
      this.definition.elemento=''
      this.definition.desc=''
      this.definition.wac=''
      this.definition.tag=''
      this.definition.exemplo=''
      this.definition.procurar=''
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
        if(this.definition.elemento){
            if (this.definition.elemento.length > 0 && this.definition.desc.length > 0 && this.definition.wac.length > 0  && this.definition.tag.length>0 && this.definition.exemplo.length > 0 && this.definition.procurar){
                return false
            }
            else
                return true
        }else{
            return true
        }
    } 
  }
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
</style>
