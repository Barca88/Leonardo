<template>
    <v-card>
        <v-navigation-drawer app
          clipped
          v-if="drawerOn"
          permanent
          :expand-on-hover="expandOnHover"
          :mini-variant="miniVariant"
          color='#2A3F54'
          class="navBar"
        >
          <v-list
            nav
            dense
            dark
          >
            <v-divider light></v-divider>
            <v-list-item link to="/admin/homeAdmin">
              <v-list-item-icon>
                <v-icon>mdi-home</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.home')}}</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/admin/import">
              <v-list-item-icon>
                <v-icon>mdi-import</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.import')}}</v-list-item-title>
            </v-list-item>
            <v-list-group
              class="white--text"
              prepend-icon="mdi-folder-open"
              :value="false"
              no-action
            >
              <template v-slot:activator>
                <v-list-item-title class="white--text">{{$t('navd.documents')}}</v-list-item-title>
              </template>
                  <v-list-item link to="/admin/folios">
                    <v-list-item-title class="white--text">{{$t('navd.folios')}}</v-list-item-title>
                  </v-list-item>
                  <v-list-item link to="/admin/compFolios">
                    <v-list-item-title class="white--text">{{$t('navd.cf')}}</v-list-item-title>
                  </v-list-item>
            </v-list-group>
            <v-list-group
              class="white--text"
              prepend-icon="mdi-format-list-bulleted-square"
              :value="false"
              no-action
            >
              <template v-slot:activator>
                <v-list-item-title class="white--text">{{$t('navd.index')}}</v-list-item-title>
              </template>
                <v-list-item link to="/admin/folios/indices">
                  <v-list-item-title class="white--text">{{$t('navd.indexes')}}</v-list-item-title>
                </v-list-item>
                <v-list-item link @click="reindexar = true">
                  <v-list-item-title class="white--text">{{$t('navd.ib')}}</v-list-item-title>
                </v-list-item>
                <v-dialog v-model="reindexar" scrollable width="500" persistent>
                  <v-card>
                    <v-toolbar color="#2A3F54" dark>
                      <h2>{{ $t('navd.ib') }}</h2>
                    </v-toolbar>
                    <v-row>
                      <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                        <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
                      </v-col>
                      <v-col>
                        <v-card-text>
                          <h3>{{ $t('navd.ibquestion') }}</h3>
                        </v-card-text>
                      </v-col>
                    </v-row>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-btn class="mr-5" @click="reindexar = false;reindFunc();runningDialog = true" v-on="{ ...tooltip}">
                            <v-icon>mdi-check</v-icon>
                          </v-btn>
                        </template>
                        <span>
                          {{$t('navd.confirm')}}
                        </span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-btn @click="reindexar = false" v-on="{ ...tooltip}">
                            <v-icon>mdi-exit-to-app</v-icon>
                          </v-btn>
                        </template>
                        <span>
                          {{$t('navd.nao')}}
                        </span>
                      </v-tooltip>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <v-dialog v-model="runningDialog" scrollable width="500" persistent>
                  <v-card>
                    <v-toolbar color="#2A3F54" dark>
                      <h2>{{ $t('navd.ib') }}</h2>
                    </v-toolbar>
                    <v-row>
                      <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                        <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                      </v-col>
                      <v-col>
                        <v-card-text>
                          <h3>{{ $t('navd.ibprogress') }}</h3>
                        </v-card-text>
                      </v-col>
                    </v-row>
                  </v-card>
                </v-dialog>
                <v-dialog v-model="successDialog" scrollable width="500" persistent>
                  <v-card>
                    <v-toolbar color="#2A3F54" dark>
                      <h2>{{ $t('navd.ib') }}</h2>
                    </v-toolbar>
                    <v-row>
                      <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                        <v-icon x-large color="#26B99A" dark>mdi-checkbox-marked</v-icon>
                      </v-col>
                      <v-col>
                        <v-card-text>
                          <h3>{{ $t('navd.ibsuccess') }}</h3>
                          <h5>{{ $t('navd.ibnDocs') }} {{nDocs}}</h5>
                          <h5>{{ $t('navd.ibnInds') }} {{nInds}}</h5>
                        </v-card-text>
                      </v-col>
                    </v-row>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-btn @click="successDialog = false" v-on="{ ...tooltip}">
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
            </v-list-group>
            <v-list-group
              class="white--text"
              prepend-icon="mdi-note-multiple"
              :value="false"
              no-action
            >
              <template v-slot:activator>
                <v-list-item-title class="white--text">{{$t('navd.annotations')}}</v-list-item-title>
              </template>
              <v-list-item link to="/admin/tagging">
                <v-list-item-title class="white--text">{{$t('navd.etags')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/tagging/tags/dicionario">
                <v-list-item-title class="white--text">{{$t('navd.eListaTags')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/tagging/tags/lista">
                <v-list-item-title class="white--text">{{$t('navd.tags')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/tagging/regras/lista">
                <v-list-item-title class="white--text">{{$t('tagging.regras')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/tagging/anotaBase">
                <v-list-item-title class="white--text">{{$t('navd.ebase')}}</v-list-item-title>
              </v-list-item>
            </v-list-group>
             <v-list-group
              class="white--text"
              prepend-icon="mdi-map-marker"
              :value="false"
              no-action
            >
              <template v-slot:activator>
                <v-list-item-title class="white--text">{{$t('navd.georef')}}</v-list-item-title>
              </template>
                  <v-list-item link to="/admin/localidades">
                    <v-list-item-title class="white--text">{{$t('navd.local')}}</v-list-item-title>
                  </v-list-item>
                  <v-list-item link to="/admin/mapas">
                    <v-list-item-title class="white--text">{{$t('navd.maps')}}</v-list-item-title>
                  </v-list-item>
                  <v-list-item link to="/admin/processamento">
                    <v-list-item-title class="white--text">{{$t('navd.processamento')}}</v-list-item-title>
                  </v-list-item>
            </v-list-group>
            <v-list-group
              class="white--text"
              prepend-icon="mdi-magnify"
              :value="false"
              no-action
            >
              <template v-slot:activator>
                <v-list-item-title class="white--text">{{$t('navd.analysis')}}</v-list-item-title>
              </template>
              <v-list-item link to="/admin/analise">
                <v-list-item-title class="white--text">{{$t('nav.barraPesquisa')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/pesquisas">
                <v-list-item-title class="white--text">{{$t('navd.estatisticas')}}</v-list-item-title>
              </v-list-item>
            </v-list-group>
            <v-list-group
              class="white--text"
              prepend-icon="mdi-account-multiple"
              :value="false"
              no-action
            >
              <template v-slot:activator>
                <v-list-item-title class="white--text">{{$t('navd.users')}}</v-list-item-title>
              </template>
              <v-list-item link to="/admin/users">
                <v-list-item-title class="white--text">{{$t('navd.guser')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/uAtivos">
                <v-list-item-title class="white--text">{{$t('navd.uativo')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/pedidos">
                <v-list-item-title class="white--text">{{$t('navd.puser')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/histAcesso">
                <v-list-item-title class="white--text">{{$t('navd.hacesso')}}</v-list-item-title>
              </v-list-item>
            </v-list-group>
            <v-list-item link to="/admin/definitions">
              <v-list-item-icon>
                <v-icon>mdi-cog</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.definitions')}}</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/admin/documentacao">
              <v-list-item-icon>
                <v-icon>mdi-text-box-multiple</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.docum')}}</v-list-item-title>
            </v-list-item>
            <v-list-item link @click="about = true">
              <v-list-item-icon>
                <v-icon>mdi-information-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.about')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="about = false" v-model="about" scrollable width="500">
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h2>{{ $t('nav.sabermais') }}</h2>
                </v-toolbar>

                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>

                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoSaberMais') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="about=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-list-item link @click="credits = true">
              <v-list-item-icon>
                <v-icon>mdi-account-group</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.credits')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="credits = false"  v-model="credits" scrollable width="500">
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h2>{{ $t('nav.creditos') }}</h2>
                </v-toolbar>
                
                <v-divider
                class="mx-4"
                horizontal
                ></v-divider>
                
                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoCreditos') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="credits=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-list-item link @click="terms = true">
              <v-list-item-icon>
                <v-icon>mdi-book-multiple</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.terms')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="terms = false" v-model="terms" scrollable  width="500">
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h2>{{ $t('nav.termos') }}</h2>
                </v-toolbar>

                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>

                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoTermos') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="terms=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-list-item link @click="priv = true">
              <v-list-item-icon>
                <v-icon>mdi-incognito</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.priv')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="priv = false" v-model="priv" scrollable width="500"> 
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h2>{{ $t('nav.privacidade') }}</h2>
                </v-toolbar>
                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>

                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoPriv') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="priv=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-list>
          <!-- <template v-slot:append v-if="hover == true"> -->
          <template v-slot:append>
            <div class="pa-2">
              <v-tooltip top> 
                <template v-slot:activator="{ on }">
                  <v-btn dark depressed min-width="60px" @click="fixNav()" v-on="on">
                    <v-icon>mdi-axis-arrow-lock</v-icon>
                  </v-btn>
                </template>
                <span>{{$t('navd.fixMenu')}}</span>
              </v-tooltip>
              <v-tooltip top> 
                <template v-slot:activator="{ on }">
                  <v-btn dark depressed min-width="60px" @click="logout();" v-on="on">
                    <v-icon>mdi-power</v-icon>
                  </v-btn>
                </template>
                <span>{{$t('navd.exit')}}</span>
              </v-tooltip>
            </div>
          </template>

        </v-navigation-drawer>
    </v-card>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return{
            title: 'Vue',
            userPic: '',
            nome: this.$store.state.user._id,
            miniVariant: true,
            expandOnHover: true,
            drawerOn: true,
            reindexar:false,
            priv:false,
            terms:false,
            credits:false,
            about:false,
            successDialog:false,
            nDocs:0,
            nInds:0,
            runningDialog:false
            // hover:false
        }
    },
    created(){
      axios.get(`https://tommi2.di.uminho.pt/api/users/foto/${this.$store.state.user._id}`, {
        responseType:'arraybuffer',
        headers: {
            'Authorization': `Bearer: ${this.$store.state.jwt}`
        }
      })
      .then(response => {
        var image = new Buffer(response.data, 'binary').toString('base64')
        this.userPic = `data:${response.headers['content-type'].toLowerCase()};base64,${image}`
      }).catch(e => {
        //console.log(e)
        this.errors.push(e)
      })
    },
    methods:{
      reindFunc: function(){
        axios.get(`https://tommi2.di.uminho.pt/api/import/reindex/`,{headers:{
          Authorization:`Bearer: ${this.$store.state.jwt}`
        }})
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            if (response.data.message === 'ok'){
              axios.get(`https://tommi2.di.uminho.pt/api/folios/folios?nome=${this.$store.state.user._id}`,{headers:{
                Authorization:`Bearer: ${this.$store.state.jwt}`
              }})
              .then(response => {
                  this.nDocs = response.data.folios.length
              }).catch(e => {
                  this.errors.push(e)
              })
              axios.get(`https://tommi2.di.uminho.pt/api/folios/index?nome=${this.$store.state.user._id}`,{headers:{
                'Content-Type': 'multipart/form-data',
                Authorization:`Bearer: ${this.$store.state.jwt}`
              }})
              .then(response => {
                  this.nInds = response.data.indexs.length
              }).catch(e => {
                  this.errors.push(e)
              })
              this.runningDialog = false
              this.successDialog = true
            }
            else{
              alert("Algo correu mal")
            }

        }).catch(e => {
            //console.log(e)
            this.errors.push(e)
        })
      },
      logout: function(){
        //console.log("destroy token here")
        this.$store.commit("guardaTokenUtilizador", "")
        this.$store.commit("guardaNomeUtilizador", "")
        this.$router.push( {path:`/admin/login`})
      },
      fixNav: function(){
        this.expandOnHover=!this.expandOnHover
        this.miniVariant=!this.miniVariant
        this.drawerOn=false
        this.$nextTick(() =>
          this.drawerOn = true
        )
      }
    }
};
</script>

<style scoped>

header{
    background:#2A3F54;
    padding: 10px;
}

h1{
    color:white;
    text-align:center;
}
.navBar{
  text-align: left;
}
.ava{
  margin-top: 50px;
}

</style>
