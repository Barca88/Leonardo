<template>
  <div id="registar">
      <v-card height="100%" width="100%">
        <v-toolbar color="#2A3F54" dark>
          <h1>{{$t('navd.pedidos')}}</h1>
        </v-toolbar>
        <v-card-title v-if= "value === 'adicionar'">
          <h3>{{$t('pForm.aU')}}</h3>
        </v-card-title>
        <v-card-title v-else-if= "value === 'ver'">
          <h3>{{$t('pForm.vU')}}</h3>
        </v-card-title>
        <v-card-title v-else>
          <h3>{{$t('pForm.eU')}}</h3>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container>
                  <v-simple-table class="table">
                    <template v-slot:default>
                        <tbody>
                            <tr>
                                <td class="text-left"><b>{{$t('users.id')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{pedido.username}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('users.nome')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{pedido.nome}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('users.email')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{pedido.email}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('p1.tipo')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{pedido.tipo}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('reg.uni')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{pedido.universidade}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('reg.dep')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{pedido.departamento}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('reg.obs')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{pedido.observacoes}}
                                    </v-layout>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                  </v-simple-table>
                  <br>
                  <!-- <v-btn ref="submit" color="#26B99A" class="white--text" @click="post();emiteFecho();">{{$t('p1.acept')}}</v-btn>
                  <v-btn color="#c9302c" class="white--text" @click="emiteFecho">{{$t('indForm.close')}}</v-btn> -->
              </v-container>
          </v-form>
        </v-card-actions>
        <v-row>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
                <v-btn class="ml-10 mb-5" ref="submit" @click="post()" v-on="{ ...tooltip}"><v-icon>mdi-check</v-icon></v-btn>
            </template>
            <span>
                {{$t('uF.conf')}}
            </span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
                <v-btn @click="dialogHelp=true" v-on="{ ...tooltip}" class="mr-5 ml-5 mb-5"><v-icon>mdi-help</v-icon></v-btn>
            </template>
            <span>
                {{$t('p1.ajuda')}}
            </span>
          </v-tooltip>
          <v-dialog @keydown.esc="dialogHelp = false"  v-model="dialogHelp" scrollable width="500">
            <v-card>
              <v-toolbar color="#2A3F54" dark>
                  <h2>{{$t('navd.pedidos')}}</h2>
              </v-toolbar>
              <v-row>
              <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                  <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
              </v-col>
              <v-col>
                  <v-card-text>
                  <h3>Ajuda da Gestão de Pedidos de Acesso</h3>
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
//import { required, email, max } from 'vee-validate/dist/rules'
//import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
// @ is an alias to /src

export default {
  data(){
    return{
      pedido:{
        username:"",
        nome:"",
        pw:"",
        email:"",
        tipo:"",
        universidade:"",
        departamento:"",
        foto:{},
        curriculo:{},
        observacoes:""
      },
      dialogHelp:false,
      valid:true,
      rules: {
          required: value => !!value || 'Required.',
          email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            if(pattern.test(value)){
              this.valid = true
            }else{
              this.valid = false
            }
            return pattern.test(value) || 'Invalid e-mail.'
          },
      },
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
  },
  methods:{
        onUpdate(){
            //console.log(typeof this.value)
            //console.log('VALUE: ' + this.value)
            //console.log(this.passedData.email)
            this.pedido.username = this.passedData._id
            this.pedido.nome = this.passedData.nome
            this.pedido.email = this.passedData.email
            this.pedido.pw = this.passedData.password
            this.pedido.tipo = this.passedData.tipo
            this.pedido.universidade = this.passedData.universidade
            this.pedido.departamento = this.passedData.departamento
            this.pedido.observacoes = this.passedData.obs
        },
        atualizarInfo(){
            //console.log('ola')
            this.$emit('atualizarInfo')
        },
        post(){
            axios.get(`https://tommi2.di.uminho.pt/api/users/pedidos/mover/` + this.pedido.username + `?nome=` + this.pedido.username,{ headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
            .then(response => {
                // JSON responses are automatically parsed.
                //console.log(response.data)
                this.pedidos = response.data.pedidos
                this.atualizarInfo
            }).catch(e => {
                //console.log(e)
                this.errors.push(e)
            })
        },
        emiteFecho(){
          this.$emit('emiteFecho')
        }
  },
  created(){
    this.onUpdate()
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
  #checkboxes input{
            display: inline-block;
            margin-right: 10px;
  }
  #checkboxes label{
            display: inline-block;
  }
</style>
