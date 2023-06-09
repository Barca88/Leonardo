<template>
   
    <v-container fluid v-bind:style="{ backgroundColor: background_color, height: height }">
       <AppHeader></AppHeader>
       <NavDraw></NavDraw>
      <h2 style="font-size: 2.0em; color: lightgrey" class="ml-6">Avaliação de Conhecimento</h2>
      <SubdomainsSelect :info="info" @showDomainsSelectPage="change_component" v-if="show_subom_page == 1"/>
      <template v-else>
        <v-container v-if="dialog_about" class="d-flex justify-center" style="position: absolute; z-index: 9">
          <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
            <ModalLayout :desc="'Acerca'" :symbol="'fa fa-info-circle'" :buttonCode="'2.2'" v-on:quit="dialog_about = false"/>
          </vue-draggable-resizable>
        </v-container>
        <v-container v-if="dialog_help" class="d-flex justify-center" style="position: absolute; z-index: 9">
          <vue-draggable-resizable style="border: 0px solid black; width: 600px" :resizable="false" :disable-user-select="false">
            <ModalLayout :desc="'Ajuda'" :symbol="'mdi-lightbulb'" :buttonCode="'1.1'" v-on:quit="dialog_help = false"/>
          </vue-draggable-resizable>
        </v-container>
        <h1 style="font-size: 1.6em" class="mt-8 ml-6">Seleção de Domínio</h1>
        <div class="ml-6">
          <v-alert v-model="alert" dismissible type="error">
            Por favor, selecione um domínio
          </v-alert>
        </div>
        <v-row align="center" class="ml-3">
          <v-col class="d-flex" cols="12" sm="4">
            <v-select v-model="select" :items="this.idDomain" item-text="description" item-value="specificInfo" label="<Escolha o domínio>" :input="onDomain()" ></v-select>
          </v-col>
        </v-row>
        <v-card cols="12" flat v-bind:style="{ backgroundColor: background_color }" style="display: flex; justify-content: space-between" class="ml-6">
          <v-col cols="6">
            <v-row style="height: 150px; float: left">
              <v-card flat class="ml-0" v-bind:style="{ backgroundColor: background_color }">
                <div>
                  <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#00cc99" @click="verify_dominio" v-bind="attrs" v-on="on">
                        <v-icon>mdi-arrange-bring-forward</v-icon>
                      </v-btn>
                    </template>
                    <span>Subdomínios</span>
                  </v-tooltip>
                </div>
                <div class="mt-2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on" @click="dialog_about = !dialog_about">
                        <i class="fa fa-info-circle" style="font-size: 22px"></i>
                      </v-btn>
                    </template>
                    <span>Acerca</span>
                  </v-tooltip>
                </div>
              </v-card>
              <v-card flat class="ml-2" v-bind:style="{ backgroundColor: background_color }">
                <div>
                  <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#00cc99" @click="reload" v-bind="attrs" v-on="on">
                        <v-icon>mdi-broom</v-icon>
                      </v-btn>
                    </template>
                    <span>Limpar</span>
                  </v-tooltip>
                </div>
                <div class="mt-2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#172d44" v-bind="attrs" v-on="on" @click="dialog_help = !dialog_help">
                        <v-icon>mdi-lightbulb</v-icon>
                      </v-btn>
                    </template>
                    <span>Ajuda</span>
                  </v-tooltip>
                </div>
              </v-card>
              <v-card flat class="ml-2" v-bind:style="{ backgroundColor: background_color }">
                <div>
                  <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="white--text text-capitalize" color="#00cc99" v-bind="attrs" v-on="on">
                        <v-icon>mdi-flag-checkered</v-icon>
                      </v-btn>
                    </template>
                    <span>Terminar</span>
                  </v-tooltip>
                </div>
              </v-card>              
            </v-row>
          </v-col>
        </v-card>
      </template>
      <Footer class="mt-5"></Footer>
    </v-container>
</template>

<script>
  import SubdomainsSelect from './Subdomains_select.vue'
  import AppHeader from '@/components/header.vue'
  import ModalLayout from './Modal_layout';
  import axios from 'axios'
  import * as _ from 'lodash'
  import NavDraw from '@/components/navDraw'
  import Footer from '@/components/Footer'

  export default {
    name: 'Domains_select',

    components:{
      SubdomainsSelect, ModalLayout, NavDraw, Footer,AppHeader 
    },

    data: function () {
        return {
          domain: null,
      loading: true,
      search: '',
      Domain: [],
      idDomain: [],
      sendObject:{
        sendId:'',
        sendDomain: '',
        sendHeader: '',
      },
      valid: false,
      idUsers: [],
      idSubDomain: [],
            background_color: "#F7F7F7", height: "1000px", select: {description: ""}, specificInfo: {}, items: [], alert: false,

            user: {
              userId: "",
              userName: "",
              name: "",
              email: "",
              gender: "",
              degree: "",
              user_type: "",
            },
            domains: [], show_subom_page: 0, info: {},
            n: 21,
            blockPointerEvents: false,
            isOpen: true,
            dialog_about: false,
            dialog_help: false,
        }
    },

    async created(){
      await this.load_attributes()
      axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions`,{
            headers: {
              'Content-Type': 'multipart/form-data',
              'Access-Control-Allow-Origin': "*"    
            }
          })
        .then((response)=>{
          
          response.data.domains.forEach((obj) =>{
            this.Domain.push(obj)
            this.idDomain.push(obj._id)
          });
        },(error) =>{
            this.x = error
      });

      
    },
    methods: {
      async change_component(){
        this.show_subom_page = 0
      }, 
      onDomain(){
        if(this.sendObject.sendDomain != this.select){
          console.log(1)
          this.idSubDomain = []
          if(this.select){
            console.log(2)
            this.Domain.forEach((obj) =>{
              console.log(2.5)
              if(obj._id ==this.select){
                console.log(3)
                obj.body.forEach((sub) =>{
                  this.idSubDomain.push(sub.subdomain)
                  console.log(sub.subdomain)
                });
              }
            });
        }
      this.sendObject.sendDomain = this.select
      }

    },
      async verify_dominio(){
        if(this.select.description == ""){
          this.alert = true
          console.log('--------')
        }
        else{
          console.log(this.select)
          this.info = {
            
            domain: this.select,
            subdomains: this.idSubDomain,
            id: this.$store.state.user._id,
            username: this.$store.state.user._id,
            name: this.$store.state.user.name,
            email: this.$store.state.user.email,
            gender: 'F',
            degree: 'Miei',
            user_type: this.$store.state.user.type
          }
          this.show_subom_page = 1
        }
      },
      async load_attributes(){
        this.items.push({
                  description:'BD'
                  
                })
        this.user.userId = this.$router.history.current.query.id
        this.user.userName = this.$router.history.current.query.username
        this.user.name = this.$router.history.current.query.name
        this.user.email = this.$router.history.current.query.email
        this.user.gender = this.$router.history.current.query.gender
        this.user.degree = this.$router.history.current.query.degree                
        this.user.user_type = this.$router.history.current.query.user_type


        
      },
      async reload(){
        Object.assign(this.$data, this.$options.data.call(this))
        await this.load_attributes()
      },
      range: _.range
    }
  }
</script>

<style>
.radial-gradient-1 {
  width: 100%;
  height: 100%;
  background-image: radial-gradient(
    ellipse farthest-corner at 45px 45px,
    #00ffff 0%,
    rgba(0, 0, 255, 0) 50%,
    #0000ff 95%
  );
}
.radial-gradient-2 {
  width: 100%;
  height: 100%;
  background-image: radial-gradient(
    farthest-corner at 45px 45px,
    #ff0000 0%,
    #0000ff 100%
  );
}
table {
  border-collapse: collapse;
}
td {
  text-align: center;
  color: rgba(0, 0, 0, 0.25);
}
th {
  color: white;
  background-color: #000;
}
.blockPointerEvents {
  pointer-events: none;
}
</style>