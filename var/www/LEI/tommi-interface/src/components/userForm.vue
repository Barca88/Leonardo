<template>
  <div id="registar">
    <v-toolbar color="#2A3F54" dark>
      <h1>{{$t('navd.guser')}}</h1>
    </v-toolbar>
      <v-card v-if= "value === 'ver'">
        <v-card-title>
          <h3>{{$t('pForm.vU')}}</h3>
        </v-card-title>
        <v-container>
          <v-simple-table class="table mr-10 ml-10">
            <template v-slot:default>
                <tbody>
                    <tr>
                        <td class="text-left"><b>{{$t('reg.unome')}}</b></td>
                        <td>
                            <v-layout>
                                {{user.username}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('users.nome')}}</b></td>
                        <td>
                            <v-layout>
                                {{user.nome}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('users.email')}}</b></td>
                        <td>
                            <v-layout>
                                {{user.email}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.tipo')}}</b></td>
                        <td>
                            <v-layout>
                                {{user.tipo}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('reg.uni')}}</b></td>
                        <td>
                            <v-layout>
                                {{user.universidade}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('reg.dep')}}</b></td>
                        <td >
                            <v-layout>
                                {{user.departamento}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('reg.obs')}}</b></td>
                        <td>
                            <v-layout>
                                {{user.observacoes}}
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
          <h3>{{$t('pForm.aU')}}</h3>
        </v-card-title>
        <v-card-title v-else>
          <h3>{{$t('pForm.eU')}}</h3>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container class="ml-5">
                 <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field 
                          v-if= "value === 'adicionar'"
                          :label="$t('reg.unome')"
                          v-model="user.username"
                          :rules="[rules.required]"            
                      ></v-text-field>
                      <v-text-field 
                          v-else-if="value === 'editar'"
                          :label="$t('reg.unome')"
                          v-model="user.username"
                          :rules="[rules.required]"
                          disabled
                      ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                      <v-text-field
                          v-if= "value != 'ver'"
                          :label="$t('users.nome')"
                          v-model="user.nome"
                          :rules="[rules.required]"  
                      ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-if= "value != 'ver'"
                      :label="$t('users.email')"
                      v-model="user.email"
                      :rules="[rules.required, rules.email]"
                      required
                  ></v-text-field>
                  </v-col>
                 </v-row>
                  <v-text-field
                        v-if= "value === 'adicionar'"
                        :label="$t('reg.pw')"
                        type='password'
                        v-model="user.pw"
                        :rules="[rules.required]"      
                    ></v-text-field>
                  <v-container fluid>
                  <v-radio-group v-if= "value != 'ver'" v-model="user.tipo" row>
                      <v-radio value="Admin"></v-radio>
                      <v-radio :label="$t('reg.admin') + ' ' + 'ou' + ' ' + $t('reg.user')" value="Leitor"></v-radio>
                  </v-radio-group>
                  </v-container>
                  <v-text-field
                      v-if= "value != 'ver'"
                      :label="$t('reg.uni')"
                      :rules="[rules.required]"
                      v-model="user.universidade"
                  ></v-text-field>
                  <v-text-field
                      v-if= "value != 'ver'"
                      :label="$t('reg.dep')"
                      :rules="[rules.required]"
                      v-model="user.departamento"
                  ></v-text-field>
                  <v-row align="center" v-if= "value === 'adicionar'">
                      <label>{{$t('p1.foto')}}:</label>
                      <v-file-input show-size :label="$t('p1.f')" v-model="user.foto"></v-file-input>
                  </v-row>
                  <v-row align="center" v-if= "value === 'adicionar'">
                      <label>{{$t('p1.file')}}:</label>
                      <v-file-input show-size type="file" :label="$t('p1.file')" v-model="user.curriculo"></v-file-input>
                  </v-row>
                  <v-text-field
                      v-if= "value != 'ver'"
                      :label="$t('reg.obs')"
                      v-model="user.observacoes"
                  ></v-text-field>
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
                    <v-dialog @keydown.esc="dialogHelp = false"  v-model="dialogHelp" scrollable width="500">
                      <v-card>
                        <v-toolbar color="#2A3F54" dark>
                            <h2>{{$t('navd.guser')}}</h2>
                        </v-toolbar>
                        <v-row>
                        <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                            <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                        </v-col>
                        <v-col>
                            <v-card-text>
                            <h3>{{$t('uF.help')}}</h3>
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
      <v-dialog @keydown.esc="failureDialog = false" v-model="failureDialog" scrollable width="500"> 
        <v-card>
          <v-toolbar color="#2A3F54" dark>
            <h2>{{$t('navd.guser')}}</h2>
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
      user:{
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
      dialog:false,
      dialogHelp:false,
      valid:true,
      failureDialog:false,
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
  },methods:{
    onUpdate(){
      //console.log(typeof this.value)
      //console.log('VALUE: ' + this.value)
      //console.log(this.passedData.email)
      if(this.value != 'adicionar'){
        this.user.username = this.passedData._id
        this.user.nome = this.passedData.nome
        this.user.email = this.passedData.email
        this.user.pw = this.passedData.password
        this.user.tipo = this.passedData.tipo
        this.user.universidade = this.passedData.universidade
        this.user.departamento = this.passedData.departamento
        this.user.observacoes = this.passedData.obs
      }
      else{
        this.user.username = ''
        this.user.nome = ''
        this.user.email = ''
        this.user.pw = ''
        this.user.tipo = ''
        this.user.universidade = ''
        this.user.departamento = ''
        this.user.observacoes = ''
      }
    },
    post: function() {
      let formData = new FormData()
        formData.append('username',this.user.username)
        formData.append('name',this.user.nome)
        formData.append('password',this.user.pw)
        formData.append('email',this.user.email)
        formData.append('tipo',this.user.tipo)
        formData.append('universidade',this.user.universidade)
        formData.append('departamento',this.user.departamento)
        formData.append('foto',this.user.foto)
        formData.append('curriculo',this.user.curriculo)
        formData.append('obs',this.user.observacoes)

      if(this.value == 'editar'){
        axios.post(`https://tommi2.di.uminho.pt/api/users/editar/guardar?nome=` + this.user.username,formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`       
          }}
        )
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            this.users = response.data.users
            this.$refs.form.reset()
            this.atualizarInfo()
            //console.log('USERS: ' + this.users[0].username)
        }).catch(e => {
            this.errors.push(e)
        })
      }else if(this.value == 'adicionar'){
        axios.post('https://tommi2.di.uminho.pt/api/users/registar',formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer: ${this.$store.state.jwt}`       
          }
        }).then(data => {
            if(data.data.message){
              this.failureDialog = true
            }
            else{
              this.users = data.data.users
              this.$refs.form.reset()
              this.atualizarInfo()
            }
        }).catch(e => {
            this.errors.push(e)
        })
      }
    },
    reset () {
      this.$refs.form.reset()
      this.user.username=''
      this.user.nome=''
      this.user.pw=''
      this.user.email=''
      this.user.tipo = false
      this.user.universidade=''
      this.user.departamento=''
      this.user.foto={}
      this.user.curriculo={}
      this.user.observacoes=''
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
      if (this.valid && this.user.username.length > 0 && this.user.nome.length > 0 && this.user.pw.length > 0 && this.user.email.length > 0  && this.user.tipo)
        return false
      else
        return true
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
  #checkboxes input{
            display: inline-block;
            margin-right: 10px;
  }
  #checkboxes label{
            display: inline-block;
  }
</style>
