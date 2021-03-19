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
              <v-list-item link to="/admin/folios/indices">
                  <v-list-item-icon>
                    <v-icon>mdi-format-list-bulleted-square</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title class="white--text">{{$t('navd.indexes')}}</v-list-item-title>
              </v-list-item>
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
              <v-list-item link to="/admin/folios/tags">
                <v-list-item-title class="white--text">{{$t('navd.eListaTags')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/folios/tags">
                <v-list-item-title class="white--text">{{$t('navd.tags')}}</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/admin/users">
                <v-list-item-title class="white--text">{{$t('navd.ebase')}}</v-list-item-title>
              </v-list-item>
            </v-list-group>
            <v-list-item link to="/admin/georef">
              <v-list-item-icon>
                <v-icon>mdi-map-marker</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.georef')}}</v-list-item-title>
            </v-list-item>
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
              <v-list-item link>
                <v-list-item-title class="white--text">{{$t('navd.estatisticas')}}</v-list-item-title>
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
            <v-list-item link to="/admin/georef">
              <v-list-item-icon>
                <v-icon>mdi-map-marker</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.georef')}}</v-list-item-title>
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
              <v-list-item-title>Termos de Utilização</v-list-item-title>
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
              <v-list-item-title>Privacidade</v-list-item-title>
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
          <template v-slot:append>
            <div class="pa-2">
              <v-btn dark depressed min-width="60px" @click="fixNav()" >
                <v-icon>mdi-axis-arrow-lock</v-icon>
              </v-btn>
              <v-btn dark depressed min-width="60px" @click="logout();">
                <v-icon>mdi-power</v-icon>
              </v-btn>
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
            priv:false,
            terms:false,
            credits:false,
            about:false,
            drawerOn: true
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
h3{
    color:white;
}
.ava{
  margin-top: 50px;
}
</style>
