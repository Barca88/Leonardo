<template>
    <div class="home">
      <appHeader></appHeader>
      <div v-if="this.$store.state.user.tipo === 'Admin'" >
        <navDraw></navDraw>
      </div>
      <div v-else >
          <navDrawLeitor></navDrawLeitor>
      </div>
      <PopupTommi />
      
        <div class="text-center"> 
        <!-- Para ficar igual ao login -->
        <h2 class="change-font black--text"> {{ $t('nav.tituloProjeto') }}</h2>  
        <h5 class="change-font black--text"> {{ $t('nav.sistemaPesquisa') }} </h5>
      </div>
      
      <!-- Só para afastar 2 centrimetro o titulo da pesquisa -->
       <v-container fluid>
            <v-row>
              <v-col cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
            <v-col cols="12" md="2"> </v-col>
              </v-row>
            </v-col>
          </v-row>
       </v-container>

        <v-container fluid>
            <v-row>
              <v-col cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
            <v-col cols="12" md="2"> </v-col>
              </v-row>
            </v-col>
          </v-row>
       </v-container>
        
    
      <v-container style="padding:0">
        <v-form ref="form" lazy-validation>
        
        <v-container fluid>
            <v-row>
              <v-col cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
            <v-col cols="12" md="2"> </v-col>

            <v-col cols="12" md="6"> 
              <v-combobox
                outlined
                dense 
                class="change-font"
                clearable  
                :items="pesquisas"
                v-bind:label="$t('nav.barraPesquisa')"
                v-model="pesquisa" 
                hide-no-data
                :rules="rulesRequired($t('nav.pesquisaNaoVazia'))"
                required
              > 
              </v-combobox>          
            </v-col>

            <v-col cols="12" md="1">
              
              <v-tooltip bottom> 
                <template v-slot:activator="{ on }">
                <v-btn width=20 depressed block color="#29b89b" class="white--text change-font" @click="pesquisar" v-on="on">
                  <v-icon>mdi-magnify</v-icon>
                </v-btn>
                </template>
                <span>{{ $t('nav.buttonPesquisa') }}</span>
              </v-tooltip>
           
            </v-col> 
            <div>
            <!-- Botão de ajuda -->
            <v-col cols="12" md="1">
              <v-dialog @keydown.esc="dialog = false" v-model="dialog" scrollable width="500">
                 <template #activator="{ on: dialog }">
                  
                    <v-tooltip bottom>
                      <template #activator="{ on: tooltip }">
                        <v-btn width=43 depressed block color="#327ab7" class="white--text change-font" v-on="{ ...tooltip, ...dialog }"><v-icon>mdi-information</v-icon> </v-btn>
                      </template>
                      <span>{{$t('nav.buttonAjuda')}}</span>
                    </v-tooltip>
                
                </template>  
                
                <v-card>
                    <v-card-title class="headline change-font">{{ $t('nav.buttonAjuda') }}</v-card-title>

                     <v-divider
                      class="mx-4"
                      horizontal
                     ></v-divider>

                    <v-card-text class="change-font" style="white-space: pre-line"
                        >{{ $t('nav.textoInstrucoes') }}</v-card-text
                      >
                    <v-card-actions>
                        <v-spacer></v-spacer>
                          
                          
                          <v-tooltip bottom> 
                            <template v-slot:activator="{ on }">
                                <v-btn depressed color="white" @click="dialog=false" v-on="on">
                                  <v-icon large>mdi-door-open</v-icon>
                                </v-btn>
                              </template>
                              <span>{{ $t('nav.Sair') }}</span>
                            </v-tooltip>
                    
                    </v-card-actions>
                  </v-card>
              </v-dialog>
            </v-col>
            </div>
                  
            <v-col cols="12" md="2"> </v-col>

              </v-row>
            </v-col>
          </v-row>
        </v-container>


          <!--
          <v-row align="center" justify="center">
            <v-col cols="12" md="6">
              <v-select required v-model="selectedFolio" :items="foliosNames" v-bind:label="$t('nav.folios')"></v-select>
            </v-col>
            
            <v-col cols="12" md="3"> 
              <p>{{ $t('nav.tipoDeTexto') }}:</p>
              <v-radio-group v-model="tipo" :rules="rulesRequired($t('nav.tipoObrigatorio'))" required>
                <v-radio v-bind:label="$t('nav.primeiroTipoTexto')" value="texto"></v-radio>
                <v-radio v-bind:label="$t('nav.segundoTipoTexto')" value="contexto"></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>
          --> 

          <v-container fluid>
            <v-row>
              <v-col cols="12" class="ma-0 pa-0">
                <v-row
                  align="start"
                  justify="center"
                >
                  <v-col cols="12" md="3"> </v-col>
                
                    <v-radio-group class="change-font" v-model="tipo" row v-bind:label="$t('nav.tipoDeTexto')" :rules="rulesRequired($t('nav.tipoObrigatorio'))" required>
                      <v-radio class="change-font" v-bind:label="$t('nav.primeiroTipoTexto')" value="texto"></v-radio>
                      <v-radio class="change-font" v-bind:label="$t('nav.segundoTipoTexto')" value="contexto"></v-radio>
                    </v-radio-group>
                                
                  <v-col cols="12" md="3"> </v-col>

                </v-row>
              </v-col>
            </v-row>
          </v-container>
            
          <v-container fluid>
            <v-row>
              <v-col class="ma-0 pa-0" cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
                  <v-col cols="12" md="3"> </v-col>
                  
                    <v-radio-group class="change-font" v-model="versao" row  v-bind:label="$t('nav.versaoTexto')" :rules="rulesRequired($t('nav.tipoObrigatorio'))" required>
                       <v-radio class="change-font" v-bind:label="$t('nav.primeiraVersaoTexto')" value="todas"></v-radio>
                       <v-radio class="change-font" v-bind:label="$t('nav.segundaVersaoTexto')" value="interpretativa"></v-radio>
                       <v-radio class="change-font" v-bind:label="$t('nav.terceiraVersaoTexto')" value="semi-diplomatica"></v-radio>
                    </v-radio-group>
           
              <v-col cols="12" md="3"> </v-col>

                </v-row>
              </v-col>
            </v-row>
          </v-container> 

          
          <v-container fluid>
            <v-row>
              <v-col class="ma-0 pa-0" cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
                  <v-col cols="12" md="3"> </v-col>
                  
                    <v-col cols="12" md="2">
                      <v-select class="change-font" required v-model="selectedFolio" :items="foliosNames" v-bind:label="$t('nav.folios')"></v-select>
                    </v-col>
                  
                  <v-col cols="12" md="3"> </v-col>

                </v-row>
              </v-col>
            </v-row>
          </v-container>


          <v-container fluid>
            <v-row>
              <v-col class="ma-0 pa-0" cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
                  <v-col cols="12" md="1"> </v-col>
                  
                  <v-radio-group class="change-font" v-model="resultado" row v-bind:label="$t('nav.tipoResultado')" :rules="rulesRequired($t('nav.tipoObrigatorio'))" required> 
                    <v-radio class="change-font" v-bind:label="$t('nav.primeiroResultado')" value="periodo"></v-radio>  
                    <v-radio class="change-font" v-bind:label="$t('nav.segundoResultado')" value="linha"></v-radio> 
                    <v-radio v-bind:label="$t('nav.terceiroResultado')" value="npalavras" class="change-font"></v-radio> 
                    
                    <v-text-field 
                        outlined
                        v-bind:suffix= "$t('nav.palavras')"
                        type = "number"
                        :disabled= "resultado != 'npalavras'"
                        dense 
                        v-model="npalavras" 
                        :rules="rulePalavras($t('nav.obrigacaoNumero'))" 
                        required class="change-font" 
                        height="20" 
                    ></v-text-field>
                                 
                  </v-radio-group>      

                </v-row>
              </v-col>
            </v-row>
          </v-container>


            <!-- o v-bind:label, tive de fazer assim para conseguir traduzir o interior do campo -->
            <!--  <v-btn @click="reset">clear</v-btn> /-->
        </v-form>
      </v-container>

      <!-- Só para afastar 1 centrimetro o titulo da pesquisa -->
       <v-container fluid>
            <v-row>
              <v-col cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
            <v-col cols="12" md="2"> </v-col>
              </v-row>
            </v-col>
          </v-row>
       </v-container>
      <Footer/>
    </div>
</template>

<script>
import axios from "axios";
import NavDraw from '../components/navDraw.vue'
import Header from '../components/header.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
import PopupTommi from '../components/PopupTommi'

export default {
  name: "Home",
  components: { 
    'navDraw':NavDraw,
    'appHeader': Header,
    'PopupTommi':PopupTommi,
    'navDrawLeitor':navDrawLeitor
  },
  data() {
    return {
      pesquisa: "", 
      dialog: false,
      foliosNames: [],
      error: "",
      // não estará a mais aqui?
      inputRule: [v => v.length > 0 || "Este campo não pode estar vazio"],
      selectedFolio: "Todos",
      tipo: "texto",
      versao: "todas", 
      npalavras: "",
      resultado: "periodo", 
      pesquisas: [], 
      show: false
    };
  }, 

  mounted: function() {
    axios
      .get("https://tommi2.di.uminho.pt/api/analise/foliosnames")
      .then(dados => {
        var objects = dados.data;
        objects.map(f => this.foliosNames.push(f._id));
        this.foliosNames.unshift("Todos");
        //console.log(this.foliosNames); 
        if(localStorage.getItem('pesquisas')){ 
         //console.log("fiz get da pesquisa");
         this.pesquisas = JSON.parse(localStorage.getItem('pesquisas'));  
         this.selectedFolio = localStorage.getItem('selectedFolio');
         this.tipo = localStorage.getItem('tipo'); 
         this.versao = localStorage.getItem('versao');
         this.resultado = localStorage.getItem('resultado');
         this.npalavras = localStorage.getItem('npalavras');
        }
      })
      .catch(err => {
        this.error = err.message;
      });
  }, 
  
  methods: { 

    addPesquisa(){ 
      this.pesquisas.unshift(this.pesquisa); 
      // guardar items selecionados na pesquisa
      localStorage.setItem('selectedFolio',this.selectedFolio); 
      localStorage.setItem('tipo',this.tipo);
      localStorage.setItem('versao',this.versao);  
      localStorage.setItem('resultado',this.resultado);  
      localStorage.setItem('npalavras',this.npalavras);
      localStorage.setItem('pesquisas', JSON.stringify(this.pesquisas));
      //console.log(this.pesquisas)
      this.pesquisa = '';
    }, 

    pesquisar() {
      //aqui vamos ver os campos e conforme os campos fazer pedidos distintos à API e redirecionar para a pag de resultados
      if (this.$refs.form.validate()) {
        let params; 
        if(this.resultado != "npalavras")  { 
          params = {
                pesquisa: this.pesquisa,
                selectedFolio: this.selectedFolio, 
                tipo: this.tipo, 
                versao: this.versao, 
                resultado: this.resultado 
            }
        } else { 
            // quando escolhe x palavras
            params = {
                pesquisa: this.pesquisa,
                selectedFolio: this.selectedFolio, 
                tipo: this.tipo, 
                versao: this.versao, 
                resultado: this.resultado, 
                npalavras: this.npalavras
            }
        } 
        this.addPesquisa();
        // chama a página dos resultados 
        this.$router.push({
            name: 'AdminResultados',
            params: params,
            
        });
       
      }
    }, 
    reset() {
      this.$refs.form.reset();
    }, 
    
    // função auxiliar que permite a tradução da obrigatoriedade dos campos
    rulesRequired(role) {
      return [value => !!value || role];
    }, 
    
    rulePalavras(role){ 
      if(this.resultado == "npalavras"){ return  [v => v > 0 || role];}
    }
    }  
};
</script>

<style lang="stylus" scoped>
.change-font {
    font-family: "Arial"; 
}
</style> 

<!-- Este CSS muda globalmente o tamanho da fonte da letra -->
<style>
.v-input .v-label {
    font-size: 0.9em;
}
</style>

<!-- CSS para questões de paddings, etc -->

<style scoped> 

.container{ 
  padding: 0px;
} 
.col-xl, .col-xl-auto, .col-xl-12, .col-xl-11, .col-xl-10, .col-xl-9, .col-xl-8, .col-xl-7, .col-xl-6, .col-xl-5, .col-xl-4, .col-xl-3, .col-xl-2, .col-xl-1, .col-lg, .col-lg-auto, .col-lg-12, .col-lg-11, .col-lg-10, .col-lg-9, .col-lg-8, .col-lg-7, .col-lg-6, .col-lg-5, .col-lg-4, .col-lg-3, .col-lg-2, .col-lg-1, .col-md, .col-md-auto, .col-md-12, .col-md-11, .col-md-10, .col-md-9, .col-md-8, .col-md-7, .col-md-6, .col-md-5, .col-md-4, .col-md-3, .col-md-2, .col-md-1, .col-sm, .col-sm-auto, .col-sm-12, .col-sm-11, .col-sm-10, .col-sm-9, .col-sm-8, .col-sm-7, .col-sm-6, .col-sm-5, .col-sm-4, .col-sm-3, .col-sm-2, .col-sm-1, .col, .col-auto, .col-12, .col-11, .col-10, .col-9, .col-8, .col-7, .col-6, .col-5, .col-4, .col-3, .col-2, .col-1{ 
  padding: 5px;
} 

.col-md-1 { 
  max-width: 53px;
}
</style>