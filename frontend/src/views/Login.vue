<template>
  <div>
    <loginHeader :ajuda='ajuda'></loginHeader>

    <v-row class="pt-10" justify="space-around"> 
      <v-col cols="12" sm="4">
        <v-img class="center" src="@/assets/leonardo_logo.png" max-height="500px" max-width="500px" @click="popup = true"/>
        <div class="text">
        <v-badge
          color="green"
          x-large
          content="2"
        >
          <h1>{{ $t('navd.tituloProjeto') }}</h1>
        </v-badge>
          <h5>{{ $t('login.adminSystem') }}</h5>
        </div>
      </v-col>
      <v-col cols="12" sm="4" align-self="end"> 
        <v-form ref="form" method="login">
        <v-text-field
          color="blue"
          outlined
          label="User"
          prepend-inner-icon="mdi-account"
          v-model="id"
          @keydown.enter="postLogin"
          required            
          ></v-text-field>
        <v-text-field
          color="blue"
          outlined
          prepend-inner-icon="mdi-lock"
          label="Password"
          type='password'
          v-model="password"
          @keydown.enter="postLogin"
          required            
          ></v-text-field>
        <v-btn 
          depressed 
          block
          x-large
          color="#26B99A" 
          class="white--text" 
          @keydown.enter="postLogin" 
          @click="postLogin">{{$t('login.enter')}}</v-btn>
        </v-form>
      </v-col>
    </v-row>
    <v-divider class="my-5"></v-divider>


    <!-- Daqui para cima -->
    <div style="text-align:center">
      <v-tooltip bottom>
        <template v-slot:activator="{ on: tooltip }">
          <v-btn text v-on="{ ...tooltip}" class="mr-5" style="background-color:lightgray" @click="dialogPW = true">
            <v-icon>mdi-lock-reset</v-icon>
          </v-btn >
        </template>
        <span>{{$t('login.rec')}}</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on: tooltip }">
          <v-btn text v-on="{ ...tooltip}" style="background-color:lightgray" @click="dialogPedido = true">
            <v-icon>mdi-text-box-check</v-icon>
          </v-btn >
        </template>
        <span>{{$t('login.reqacesso')}}</span>
      </v-tooltip>
    </div>
    <v-dialog
      v-model="dialogPW"
      scrollable 
      width="500"
      persistent
    >
      <v-card>
        <v-toolbar color="#2A3F54" dark>
          <h1>Login</h1>
        </v-toolbar>
        <v-row>
          <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
            <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
          </v-col>
          <v-col>
            <v-card-text>
              <h3>{{$t('login.pCred')}}</h3>
            </v-card-text>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn color="#c9302c" dark @click="dialogPW = false" to="/login" v-on="{ ...tooltip}">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </template>
            <span>
              {{$t('indForm.close')}}
            </span>
          </v-tooltip>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="dialogPedido"
      scrollable 
      width="700"
      persistent
    >
      <v-card height="100%" width="100%">
        <v-toolbar color="#2A3F54" dark>
          <h1>{{$t('reg.pag')}}</h1>
        </v-toolbar>
        <v-card-actions>
          <v-row
            class="fill-height"
            align="center"
            justify="center"
          >
            <div style="width:500px">
              <v-form ref="form" method="post" enctype="multipart/form-data">
                  <v-container>
                      <v-row>
                        <v-text-field
                            label= "Username"
                            v-model="pedido.username"
                            :rules="[rules.required]"
                            required                      
                        ></v-text-field>
                        <h5 style="color:red">*</h5>
                      </v-row>
                      <v-row>
                        <v-text-field
                        label="Password"
                        type='password'
                        v-model="pedido.pw"
                        :rules="[rules.required]"            
                        ></v-text-field>
                        <h5 style="color:red">*</h5>
                      </v-row>
                      <v-row>
                        <v-text-field
                            label="Nome"
                            v-model="pedido.nome"
                            :rules="[rules.required]"                    
                        ></v-text-field>
                        <h5 style="color:red">*</h5>
                      </v-row>
                       <v-row>
                        <v-text-field
                            label="Número de Aluno"
                            v-model="pedido.studentNumber"
                            :rules="[rules.required]"                    
                        ></v-text-field>
                        <h5 style="color:red">*</h5>
                      </v-row>
                      <v-row>
                        <v-text-field
                            label="Email"
                            v-model="pedido.email"
                            :rules="[rules.required, rules.email]"
                            required                     
                        ></v-text-field>
                        <h5 style="color:red">*</h5>
                      </v-row>
                      <v-container fluid>
                        <v-row>
                          <label>{{$t('reg.tipo')}}</label>
                          <h5 style="color:red">*</h5>
                        </v-row>
                        <v-radio-group v-model="pedido.tipo" :rules="[rules.required]" column >
                            <v-radio label="Admin" value="Admin"></v-radio>
                            <v-radio label="Teacher" value="Teacher"></v-radio>
                            <v-radio label="Student" value="Student"></v-radio>
                            <v-radio label="Leitor" value="Leitor"></v-radio>
                        </v-radio-group>
                      </v-container>
                      <v-row>
                        <v-text-field
                            label="Universidade"
                            :rules="[rules.required]"
                            v-model="pedido.universidade"             
                        ></v-text-field>
                        <h5 style="color:red">*</h5>
                      </v-row>
                      <v-row>
                        <v-text-field
                            label="Departamento"
                            :rules="[rules.required]"
                            v-model="pedido.departamento"                      
                        ></v-text-field>
                        <h5 style="color:red">*</h5>
                      </v-row>
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
                          v-model="pedido.comments"                     
                      ></v-text-field>
                      <br>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-btn class="mr-5 mb-10 mt-10" @click.prevent="reset" v-on="{...tooltip}">
                            <v-icon>mdi-history</v-icon>
                          </v-btn>
                        </template>
                        <span>
                          {{$t('login.re')}}
                        </span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-btn class="mr-5 mb-10 mt-10" @click="post();" v-on="{ ...tooltip}" :disabled="disableButton">
                            <v-icon>mdi-check</v-icon>
                          </v-btn>
                        </template>
                        <span>
                          {{$t('login.sub')}}
                        </span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-btn class="mb-10 mt-10" @click="dialogPedido = false" v-on="{ ...tooltip}">
                            <v-icon>mdi-exit-to-app</v-icon>
                          </v-btn>
                        </template>
                        <span>
                          {{$t('indForm.close')}}
                        </span>
                      </v-tooltip>
                  </v-container>
              </v-form>
            </div>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="dialog"
      scrollable 
      width="500"
      persistent
    >
      <v-card>
        <v-toolbar color="#2A3F54" dark>
          <h1>Login</h1>
        </v-toolbar>
        <v-row>
          <v-col style="margin-left:1cm;max-width:20px; margin-top:15px" >
            <v-icon x-large color="#c9302c" dark>mdi-close</v-icon>
          </v-col>
          <v-col>
            <v-card-text class="mt-2">
              {{$t('login.uInv')}}
            </v-card-text>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn @click="dialog = false" to="/login" v-on="{ ...tooltip}">
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
              {{$t('login.new')}}
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
    <v-container/>
    <appFooter></appFooter>
  </div>
</template>
<script>
import axios from 'axios'
import loginHeader from '../components/headerLogin.vue'
import Footer from '../components/footer2.vue'
export default {  
  data(){
    return {
      id : "",
      password : "",
      dialog: false,
      ajuda:'login',
      popup:false,
      dialogPW:false,
      dialogPedido:false,
      pedido:{
        username:"",
        nome:"",
        studentNumber:"",
        pw:"",
        email:"",
        tipo:"",
        universidade:"",
        departamento:"",
        foto:{},
        curriculo:{},
        comments:""
      },
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
    this.pedido.comments=''
  },
  methods:{
    postLogin: function () {
      let formData = new FormData()
        formData.append('id',this.id)
        formData.append('password',this.password)
      axios.post(`${process.env.VUE_APP_BACKEND}/login`,formData,{
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization:`Bearer: ${this.$store.state.jwt}`,
            'Access-Control-Allow-Origin': "*"     
        }
      }).then(data => {
          if (data.data.error){
            this.$refs.form.reset()
            this.dialog = !this.dialog
          }
          else if(data.data.token!=undefined){ // &&data.data.users
            this.$store.commit("guardaTokenUtilizador", data.data.token)
            this.$store.commit("guardaNomeUtilizador", data.data.user)
            this.$store.commit('set_user',  data.data.user) 
            
            console.log('-----USER')
            console.log(data.data.user)
            this.$router.push( {path:`/`})
          }
      }).catch(e => {
          console.log(e);
})
    },
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
            formData.append('obs',this.pedido.comments)
            formData.append('studentNumber',this.pedido.studentNumber)

        axios.post(`${process.env.VUE_APP_BACKEND}/users/pedidos/registar`,formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': "*"    
          }
        }).then(data => {
          if(data.data.message){
              this.failureDialog = true
            }
          else{
            this.dialogPedido = false
            this.$refs.form.reset()
            this.$router.push( {path:`/login`})
          }
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
      this.pedido.comments=''
    }
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
    'loginHeader': loginHeader,
    'appFooter':Footer
  }
}
</script>
<style scoped>
  #login *{
            box-sizing: border-box;
  }
  #form{
            margin: 20px auto;
            max-width: 500px;
  }
  #links{
            margin: 20px auto;
            max-width: 1000px;
            justify-content: centerd;
  }

  .text{
    text-align: center;
  }
  .centered {
      text-align: center;
      width: 100%;
  }

  .center {
    margin-top: 2cm;
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 50%;
  }

  .centered_tab {
      float:none; /*to make sure there is no active float*/
      display: inline-block;
  }
  #checkboxes input{
            display: inline-block;
            margin-right: 10px;
  }
  #checkboxes label{
            display: inline-block;
  }
</style>
