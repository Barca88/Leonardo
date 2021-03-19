<template>
  <div>
    <appHeader></appHeader>
    <div v-if="this.$store.state.user.tipo === 'Admin'" >
        <navDraw></navDraw>
    </div>
    <div v-else >
        <navDrawLeitor></navDrawLeitor>
    </div>
    <v-container>
    <div id="imprimeMain">
    <v-row>
      <v-col col="12">
        <div class="results">
          
          <v-img :src="require('../assets/logo_original.png')" contain width="150px"></v-img> 

        
          <h2 class="change-font black--text"> 
            {{ $t('nav.tituloProjeto') }}
          </h2> 
          
        
          <h3 class="font-weight-light change-font"> 
            {{ $t('nav.ResultadosAnalise') }}
          </h3> 
          
          
          <h3 class="font-weight-light change-font">
            {{ $t('nav.resultadoPara') }} 
            <span class="font-weight-black change-font">{{this.pesquisa}}</span>
          </h3>  
          
          <h3 class="font-weight-light change-font">
            {{ $t('nav.Parametros') }}
            <span class="font-weight-black change-font">{{this.$route.params.selectedFolio}}, {{this.$route.params.tipo}}, {{this.$route.params.versao}}, {{this.$route.params.resultado}}</span>
          </h3>  
          
          <h5 class="change-font blue--text text--darken-4">
            {{this.numResultados}} {{ $t('nav.resultadosEm') }} {{ this.tempoFinal }} {{ $t('nav.milisegundos') }}
          </h5>

        
        
        <v-container fluid>
            <v-row>
                <v-row
                  align="start"
                  justify="end"
                >
              
            <v-col cols="12" md="1">            
              <v-tooltip bottom> 
                <template v-slot:activator="{ on }">
                <v-btn depressed block color="#29b89b" class="white--text change-font" @click="goHome" v-on="on">
                  <v-icon>mdi-magnify</v-icon>
                </v-btn>
                </template>
                <span>{{ $t('nav.buttonPesquisa') }}</span>
              </v-tooltip>
           
            </v-col> 

              
            <!-- Botão de ajuda -->
            <v-col cols="12" md="1">
              
              <v-dialog @keydown.esc="dialog = false" v-model="dialog" scrollable width="500">
                 <template #activator="{ on: dialog }">
                  
                    <v-tooltip bottom>
                      <template #activator="{ on: tooltip }">
                        <v-btn depressed block color="#327ab7" class="white--text change-font" v-on="{ ...tooltip, ...dialog }"><v-icon>mdi-information</v-icon> </v-btn>
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
            

            <v-col cols="12" md="1">
              
              <v-tooltip bottom> 
                <template v-slot:activator="{ on }">
                <v-btn depressed block color="#29b89b" class="white--text change-font" @click="printSection" v-on="on">
                  <v-icon>mdi-printer</v-icon>
                </v-btn>
                </template>
                <span>{{ $t('nav.imprimir') }}</span>
              </v-tooltip>
           
            </v-col> 

            <!-- Para ficar em cima do painel -->  
            <v-col cols="12" md="1"> </v-col>

            </v-row>
          </v-row>
        </v-container>
        
        </div>
        
        <v-card text class="pa-3 change-font">
          <!-- Dá warning aqui pq pode haver vários folios com a mesma key que é o id do folio --> 
          <!-- Portanto, ao fazer o indice mais o valor da id como chave então significa que não dá problemas pq resulta chave unica -->
          <div v-for="(item,index) in pageOfItems" v-bind:key="item.idfolio + index">
            <!-- se o item.periodo existe, ou seja, foi feita pesquisa por periodo inclui o periodo -->
            <h3 class="font-weight-black change-font" v-if="item.periodo">
              <a class="change-font" @click.stop="showFolio(item.idfolio)">{{ item.idfolio }}</a>
              &#x25CF;
              {{ $t('nav.resultadoLinha') }} {{ item.linha}} &#x25CF; {{ $t('nav.resultadoPeriodo') }} {{ item.periodo }}
            </h3>            

            <!-- caso contrário, se é feita pesquisa por linha não inclui o periodo -->
            <h3 class="font-weight-black change-font" v-else>
              <a class="change-font" @click.stop="showFolio(item.idfolio)">{{ item.idfolio }}</a>
              &#x25CF;
              {{ $t('nav.resultadoLinha') }} {{ item.linha}} 
            </h3> 

      
            <!-- Meter style="font-size:0.9em;" para diminuir o tamanho da fonte do resultado da pesquisa no p -->
            <p v-html="item.valor" class="font-weight-light change-font">{{ item.valor }}</p>
            <br />  
          </div>
          <div class="card-footer text-center change-font">
            <jw-pagination v-if="resultados!=null" :items="resultados" @changePage="onChangePage"></jw-pagination>
         </div>
        </v-card> 
      </v-col>
    </v-row>
    <!-- tem de estar persistent para fazer clean do array conta -->
    <v-dialog v-model="dialogFolio" @keydown.esc="dialogFolio = !dialogFolio; conta=[]" persistent scrollable max-width="800px">
      <v-card v-if="conta != null && dialogFolio">
        <v-card-title class="headline change-font" v-if="conta.length <= 1"> <span class="change-font">{{ $t('nav.folioAnaliseHeadline') }}</span>  <p> <small class="change-font">{{ this.folioAtual }},</small> <small v-for="(count,idx) in conta" :key="idx" class="keep-spaces change-font"> {{count.key}} {{$t('nav.com')}} {{count.value}} {{$t('nav.occur1')}} </small> </p> </v-card-title>
        <!-- só para acrescentar separador entre as palavaras (+1 palavra no folio) -->
        <v-card-title class="headline change-font" v-else> <span class="change-font"> {{ $t('nav.folioAnaliseHeadline') }} </span> <p> <small class="change-font">{{ this.folioAtual }}</small> <small v-for="(countElse,idx) in conta" :key="idx" class="keep-spaces change-font">, {{countElse.key}} {{$t('nav.com')}} {{countElse.value}} {{$t('nav.occur2')}}</small> </p> </v-card-title>

         <v-divider
        horizontal
       ></v-divider>

        <v-card-text v-html="textoAtual" class="change-font">{{ this.textoAtual }}</v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <!--
          <v-btn depressed text class="grey--text change-font" @click="dialogFolio = !dialogFolio; conta=[]" >{{$t('nav.fechar')}}</v-btn>
          --> 
          <v-tooltip bottom> 
            <template v-slot:activator="{ on }">
                <v-btn depressed color="white" @click="dialogFolio = !dialogFolio; conta=[]" v-on="on">
                  <v-icon large>mdi-door-open</v-icon>
                </v-btn>
              </template>
              <span>{{ $t('nav.fechar') }}</span>
          </v-tooltip>
        
        </v-card-actions>

      </v-card>
    </v-dialog>
    </div>
    <Footer/>
  </v-container>
  </div>
</template>

<script>
import axios from "axios";
import NavDraw from '../components/navDraw.vue'
import Header from '../components/header.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
export default {
  data() {
    return {
      pesquisa: "",
      page: 1,
      resultados: null,
      dialog: false,
      dialogFolio: false,
      folioAtual: null,
      textoAtual: null,  
      pageOfItems: [],
      conta: [],  
      tempoFinal: 0, 
      numResultados: 0 
    };
  },
  components: {
    'navDraw':NavDraw,
    'appHeader': Header,
    'navDrawLeitor':navDrawLeitor
  },
  created() {
    
    var tempo_inic = performance.now()
    
    this.pesquisa = this.$route.params.pesquisa;
    this.pesquisa = this.pesquisa.trim();
    var res = []; 
    axios
      .get("https://tommi2.di.uminho.pt/api/analise/pesquisa", { params: this.$route.params })
      .then(dados => {

        var tempo_fin = performance.now()
        this.tempoFinal = tempo_fin - tempo_inic 
        this.numResultados = dados.data.length 

        if(this.pesquisa.startsWith("+Tag")){ 
          
          var tagAbre = "<" + this.pesquisa.split(" ")[1] + ">"
          var tagFecho = "</" + this.pesquisa.split(" ")[1] + ">"
         
          for (x = 0; x < dados.data.length; x++) {
            dados.data[x].valor = dados.data[x].valor.replace(
              new RegExp(tagAbre, "g"),
              '<span class="red--text change-font">' 
            );  
            dados.data[x].valor = dados.data[x].valor.replace(
              new RegExp(tagFecho, "g"),
              '</span>' 
            );  
          }      

        } else if ((this.pesquisa.startsWith('"') && this.pesquisa.endsWith('"')) || this.$route.params.npalavras) {
          var sem_aspa_texto = this.pesquisa
          if (this.pesquisa.startsWith('"') && this.pesquisa.endsWith('"')){ 
            sem_aspa_texto = this.pesquisa.substring(1,this.pesquisa.length - 1);
          } 

          var x = 0;
          for (x = 0; x < dados.data.length; x++) {
            dados.data[x].valor = dados.data[x].valor.replace(
              new RegExp('<.*>', "g"),
              '' 
            );  
            dados.data[x].valor = dados.data[x].valor.replace(
              new RegExp('</.*>', "g"),
              '' 
            );  
          }      


          for (x = 0; x < dados.data.length; x++) {
            dados.data[x].valor = dados.data[x].valor.replace(
              new RegExp(sem_aspa_texto, "g"),
              '<span class="red--text change-font">' + sem_aspa_texto + "</span>"
            );  
          }      
        } else  {
         

          res = this.pesquisa.trim().split(" ");
          var j = 0;
          //console.log("Anters splitttt " + res)
          for (; j < res.length; j++) {
            if (res[j].startsWith("+")) {
              res[j] = res[j].split("+")[1];
            }
            // desnecessario, nao entre aqui caso comece com "
            else if (res[j].startsWith('"')) {
              // retira no início a aspa
              res[j] = res[j].split('"')[1];
            } else if (res[j].endsWith('"')) {
              // retira no final a aspa
              res[j] = res[j].slice(0, -1);
            }
          }

          var i = 0;

          for (x = 0; x < dados.data.length; x++) {
            dados.data[x].valor = dados.data[x].valor.replace(
              new RegExp('<.*>', "g"),
              '' 
            );  
            dados.data[x].valor = dados.data[x].valor.replace(
              new RegExp('</.*>', "g"),
              '' 
            );  
          }      

          // troquei a ordem aqui pq caso contrario não fazia negrito correto das palavras todas
          for (; i < dados.data.length; i++) {
            for (j = 0; j < res.length; j++) {
              if (dados.data[i].valor.includes(res[j])) {
                dados.data[i].valor = dados.data[i].valor.replace(
                  new RegExp(res[j], "g"),
                  '<span class="red--text change-font">' + res[j] + "</span>"
                );
              }
            }
          }
        }

        this.resultados = dados.data;
        //console.log(this.resultados)
        
      })
      .catch(err => {
        this.error = err.message;
      });
  }, 

  methods: {   

     goHome(){ 
       this.$router.push({
        name: 'Analise',          
      });
     },

     onChangePage(pageOfItems) {
          // update page of items
          this.pageOfItems = pageOfItems;
      },
    
    printSection() {
      // Pass the element id here
      this.$htmlToPaper('imprimeMain');
    },

    showFolio(idfolio) {
      this.folioAtual = idfolio;
      var result = []; 
      var tam = 0;
      axios
        .get("https://tommi2.di.uminho.pt/api/analise/folio/" + idfolio)
        .then(dados => {
          // se a pesquisa não começa por aspas não a vai partir para substituir a frase toda no folio
          
          if(this.pesquisa.startsWith("+Tag")){ 
          
            var tagAbre = "<" + this.pesquisa.split(" ")[1] + ">"
            var tagFecho = "</" + this.pesquisa.split(" ")[1] + ">"

            this.textoAtual = dados.data.textoSTags.replace(
                new RegExp(tagAbre, "g"),
                '<span class="red--text change-font">') 

            this.textoAtual = this.textoAtual.replace(
                new RegExp(tagFecho, "g"),
                '</span>')


            tam = dados.data.textoSTags.match(new RegExp(tagAbre,'g')).length

            if ( !( tagAbre in this.conta) ) {
              this.conta.push({
                key: this.pesquisa.split(" ")[1],
                value: tam
              });
            } 

            this.dialogFolio = true;
                  

        } else if (this.pesquisa.startsWith('"') && this.pesquisa.endsWith('"')) {
            
            var sem_aspa = this.pesquisa.substring(1, this.pesquisa.length - 1);
            
            
            dados.data.textoSTags = dados.data.textoSTags.replace(
            new RegExp('<.*>', "g"),
              '' 
            );  
            
            dados.data.textoSTags = dados.data.textoSTags.replace(
            new RegExp('</.*>', "g"),
              '' 
            );     


            if (dados.data.textoSTags.includes(sem_aspa)) {
              this.textoAtual = dados.data.textoSTags.replace(
                new RegExp(sem_aspa,'g'),
                '<span class="red--text change-font">' + sem_aspa + "</span>"
              );
              
              tam = dados.data.textoSTags.match(new RegExp(sem_aspa,'g')).length

              if ( !( sem_aspa in this.conta) ) {
                this.conta.push({
                  key: sem_aspa,
                  value: tam
                });
              } 

              this.dialogFolio = true;
            }
          } else {
            // se não começa por aspas parte o resultado em partes...

            result = this.pesquisa.trim().split(" ");
            //console.log(result);
            //var j = 0;
            var i = 0;
            
            dados.data.textoSTags = dados.data.textoSTags.replace(
            new RegExp('<.*>', "g"),
              '' 
            );  
            
            dados.data.textoSTags = dados.data.textoSTags.replace(
            new RegExp('</.*>', "g"),
              '' 
            );     

            // percorre a pesquisa efetuada
            for (i = 0; i < result.length; i++) {
              // se encontra o mais, retira e coloca no texto do folio o resultado do que está à frente do + a negrito
              //console.log(result[i]);
              if (result[i].startsWith("+")) {
                var s2 = result[i].substr(1);
                if (dados.data.textoSTags.includes(s2)) {
                  dados.data.textoSTags = dados.data.textoSTags.replace(
                    new RegExp(s2,'g'),
                    '<span class="red--text change-font">' + s2 + "</span>"
                  );
                  
                  tam = dados.data.textoSTags.match(new RegExp(s2,"g")).length

                  //this.conta = []
                  if ( !( s2 in this.conta) ) {
                    this.conta.push({
                      key: s2,
                      value: tam
                    });
                  } 

                  this.dialogFolio = true;
                }
              }
              // caso contrário se não tem mais nem menos então é uma pesquisa normal
              else if (
                !result[i].startsWith("+") &&
                !result[i].startsWith("-")
              ) {

                
                /* Tirei isto e deu bem quando consulta folio com texto normal, antes não dava
                
                dados.data.textoSTags = dados.data.textoSTags.replace(
                 new RegExp('<.*>', "g"),
                '' 
                );  
            
                dados.data.textoSTags = dados.data.textoSTags.replace(
                 new RegExp('</.*>', "g"),
                '' 
                );     
                
                */
                

                if (dados.data.textoSTags.includes(result[i])) {
                  dados.data.textoSTags = dados.data.textoSTags.replace(
                    new RegExp(result[i],'g'),
                    '<span class="red--text change-font">' + result[i] + "</span>"
                  );
                  
                  tam = dados.data.textoSTags.match(new RegExp(result[i],"g")).length
                  
                  if ( !( result[i] in this.conta) ) {
                    this.conta.push({
                      key: result[i],
                      value: tam
                    });
                  } 

                  this.dialogFolio = true; 
                }
              }
            } 
            
            //console.log(this.conta)
            this.textoAtual = dados.data.textoSTags          
            
          }
        })
        .catch(err => {
          this.error = err.message;
        });
    }
  }
};
</script> 

<style scoped>
.keep-spaces { white-space: pre-wrap; } 
@media print {
  body { 
    overflow: auto;
    height: auto; 
  }
  .page-break { display: block; page-break-before: always; }
}

.col-md-1 {
    margin: 10px;
    max-width: 53px;
} 

.v-application p {
    margin-bottom: 1px;
}
</style>

<style lang="stylus" scoped>
.change-font {
    font-family: "Arial";
}
</style>

