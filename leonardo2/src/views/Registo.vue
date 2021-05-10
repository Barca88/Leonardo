<template>
  <div id="registar">
    <loginHeader :ajuda='ajuda'></loginHeader>
      <v-card height="100%" width="100%">
        <v-card-title>
          <!-- <h1>Página de Registo</h1> -->
        </v-card-title>
        <v-card-actions>
            <v-row
            class="fill-height"
            align="center"
            justify="center"
            >
            <div>
                <h1>{{$t('reg.pag')}}</h1>
                <h3>{{$t('reg.quest')}}</h3>
                <v-btn depressed link to="/login">Faça o login</v-btn>
                <v-form ref="form" method="post" enctype="multipart/form-data">
                    <v-container>
                        <v-text-field
                            label= "Username"
                            v-model="pedido.username"
                            required                      
                        ></v-text-field>
                        <v-text-field
                        label="Password"
                        type='password'
                        v-model="pedido.pw"
                        required            
                        ></v-text-field>
                        <v-text-field
                            label="Nome"
                            v-model="pedido.nome"
                            required                     
                        ></v-text-field>
                        <v-text-field
                            label="Email"
                            v-model="pedido.email"
                            :rules="[rules.required, rules.email]"
                            required                     
                        ></v-text-field>
                        <v-container fluid>
                        <label>{{$t('reg.tipo')}}</label>
                        <v-radio-group v-model="pedido.tipo" column >
                            <v-radio label="Admin" value="Admin"></v-radio>
                            <v-radio label="Leitor" value="Leitor"></v-radio>
                        </v-radio-group>
                        </v-container>
                        <v-text-field
                            label="Universidade"
                            v-model="pedido.universidade"             
                        ></v-text-field>
                        <v-text-field
                            label="Departamento"
                            v-model="pedido.departamento"                      
                        ></v-text-field>
                        <v-row align="center">
                            <label>{{$t('reg.foto')}}:</label>
                            <v-file-input show-size label="File input" v-model="pedido.foto"></v-file-input>
                        </v-row>
                        <v-row align="center">
                            <label>{{$t('reg.cur')}}:</label>
                            <v-file-input show-size type="file" label="File input" v-model="pedido.curriculo"></v-file-input>
                        </v-row>
                        <v-text-field
                            label="Observações"
                            v-model="pedido.observacoes"                     
                        ></v-text-field>
                        <br>
                        <v-btn class="blue white--text" @click.prevent="reset">Reset</v-btn>
                        <v-btn ref="submit" class="green white--text" @click="post()" v-bind:class="{disabled: disableButton}" :disabled="disableButton" >Submeter</v-btn>
                    </v-container>
                </v-form>
                </div>
            </v-row>
          </v-card-actions>
      </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import Header from '../components/headerLogin.vue'
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
      dialog:false,
      ajuda:'registo',
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
  methods:{
    /*onUpdate(){
      console.log(typeof this.value)
      console.log('VALUE: ' + this.value)
      //console.log(this.passedData.email)
      if(this.value != 'adicionar'){
        this.pedido.username = this.passedData._id
        this.pedido.nome = this.passedData.nome
        this.pedido.email = this.passedData.email
        this.pedido.pw = this.passedData.password
        this.pedido.tipo = this.passedData.tipo
        this.pedido.universidade = this.passedData.universidade
        this.pedido.departamento = this.passedData.departamento
        this.pedido.observacoes = this.passedData.obs
      }
      else{
        this.pedido.username = ''
        this.pedido.nome = ''
        this.pedido.email = ''
        this.pedido.pw = ''
        this.pedido.tipo = ''
        this.pedido.universidade = ''
        this.pedido.departamento = ''
        this.pedido.observacoes = ''
      }
    },*/
    post: function() {
        let formData = new FormData()
            formData.append('username',this.pedido.username)
            formData.append('name',this.pedido.nome)
            formData.append('password',this.pedido.pw)
            formData.append('email',this.pedido.email)
            formData.append('tipo',this.pedido.tipo)
            formData.append('universidade',this.pedido.universidade)
            formData.append('departamento',this.pedido.departamento)
            formData.append('foto',this.pedido.foto)
            formData.append('curriculo',this.pedido.curriculo)
            formData.append('obs',this.pedido.observacoes)

        axios.post('http://localhost:5000/users/pedidos/registar',formData,{
          headers: {
            'Content-Type': 'multipart/form-data'    
          }
        }).then(() => {
            //console.log(data)
            this.$refs.form.reset()
            this.$router.push( {path:`/admin/login`})
        }).catch(e => {
            this.errors.push(e)
        })
    },
    reset () {
      this.$refs.form.reset()
      this.pedido.username=''
      this.pedido.nome=''
      this.pedido.pw=''
      this.pedido.email=''
      this.pedido.tipo = false
      this.pedido.universidade=''
      this.pedido.departamento=''
      this.pedido.foto={}
      this.pedido.curriculo={}
      this.pedido.observacoes=''
    }
  },
  created(){
    this.pedido.username=''
    this.pedido.nome=''
    this.pedido.pw=''
    this.pedido.email=''
    this.pedido.tipo = false
    this.pedido.universidade=''
    this.pedido.departamento=''
    this.pedido.foto={}
    this.pedido.curriculo={}
    this.pedido.observacoes=''
  },
  computed:{
    disableButton (){
        if(this.pedido.username){
            if (this.valid && this.pedido.username.length > 0 && this.pedido.nome.length > 0 && this.pedido.pw.length > 0 && this.pedido.email.length > 0  && this.pedido.tipo)
                return false
            else
                return true
        }
        else{
            return true
        }
    } 
  },
  components:{
    'loginHeader': Header,
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
            margin-bottom: 80px;
  }
  #checkboxes input{
            display: inline-block;
            margin-right: 10px;
  }
  #checkboxes label{
            display: inline-block;
  }
</style>
