<template>
    <v-app-bar app color="#2A3F54" height="100" clipped-left>
        <v-list
            nav
            dense
            dark
            color="#2A3F54"
        >
            <v-list-item two-line class="px-0">
                <v-list-item-avatar min-width="55px" tile class="ava" @click="about = true">
                    <v-img src="@/assets/logo_original.png"/>
                </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title><h2>{{$t('navd.tituloProjeto')}}</h2></v-list-item-title>
                <v-list-item-subtitle>{{$t('login.adminSystem')}}</v-list-item-subtitle>
              </v-list-item-content>
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

                    <v-card-text class="change-font" style="white-space: pre-line"
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
        </v-list>
        <div class="spacer"></div>
        <v-tooltip bottom> 
            <template v-slot:activator="{ on }">
            <v-btn text small class="white--text change-font" @click="setLocale('pt')" v-on="on">PT</v-btn>
            </template>
            <span>{{ $t('nav.LinguaPT') }}</span>
        </v-tooltip>

        <v-tooltip bottom> 
            <template v-slot:activator="{ on }">
            <v-btn text small class="white--text change-font" @click="setLocale('es')" v-on="on">ES</v-btn>
            </template>
            <span>{{ $t('nav.LinguaES') }}</span>
        </v-tooltip>
        
        <v-tooltip bottom> 
            <template v-slot:activator="{ on }">
            <v-btn text small class="white--text change-font" @click="setLocale('en')" v-on="on">UK</v-btn>
            </template>
            <span>{{ $t('nav.LinguaEN') }}</span>
        </v-tooltip>
        <v-menu>
            <template v-slot:activator="{ on: menu }">
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn
                        fab
                        v-on="{ ...tooltip, ...menu }"
                        >
                            <v-avatar>
                                <v-img v-bind:src="userPic"/>
                            </v-avatar>
                        </v-btn>
                    </template>
                    <span>
                        {{$t('header.opPerfil')}}
                    </span>
                </v-tooltip>
            </template>
            <v-list>
                <v-list-item link :to="`/admin/users/ver`">
                    <v-list-item-title>{{$t('header.vPerfil')}}</v-list-item-title>
                </v-list-item>
                <v-list-item @click="logout();" text>
                    <v-list-item-title>{{$t('head.exit')}}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
        <v-list-item-group>
            <v-list-item disabled dark>
                <v-list-item-content>
                    <v-list-item-title>{{this.$store.state.user.nome}}</v-list-item-title>
                    <v-list-item-subtitle>{{this.$store.state.user.tipo}}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
        </v-list-item-group> 
    </v-app-bar>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return{
            help: '',
            userPic: '',
            about:false
        }
    },
    props:{
        ajuda:{
            type:String
        }
    },
    methods:{
        logout: function(){
            //console.log("destroy token here")
            this.$store.commit("guardaTokenUtilizador", "")
            this.$store.commit("guardaNomeUtilizador", "")
            this.$router.push( {path:`/admin/login`})
        },
        getUrl: function(){
            var components = this.$route.path.split('/')
            components.shift()
            components.shift()
            if (components.length > 1)
                components = components.join('/')
            return components
        },
        setLocale(locale){ 
            this.$i18n.locale = locale
            this.$router.push({
                params: { lang: locale }
            })
        }
    },
    created(){
        this.userPic=''
        axios.get(`https://tommi2.di.uminho.pt/api/users/foto/${this.$store.state.user._id}?seed=${Date.now()}`, {
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

        if(this.ajuda == 'users'){
            this.help = 'Esta é a ajuda dos users'
        }
        else if(this.ajuda == 'tags'){
            this.help = 'Esta é a ajuda das tags'
        }
        else if(this.ajuda == 'perfil'){
            this.help = 'Esta é a ajuda do perfil'
        }
        else if(this.ajuda == 'folios'){
            this.help = 'Esta é a ajuda dos fólios'
        }
        else if(this.ajuda == 'about'){
            this.help = 'Esta é a ajuda da about page'
        }
        else if(this.ajuda == 'indices'){
            this.help = 'Esta é a ajuda dos índices'
        }
        else if(this.ajuda == 'imports'){
            this.help = 'Esta é a ajuda dos imports'
        }
        else if(this.ajuda == 'pedidos'){
            this.help = 'Esta é a ajuda dos pedidos de acesso'
        }
        //console.log('HELP: ' + this.help)
    }
};
</script>

<style scoped>
.v-toolbar__content, .v-toolbar__extension{
    position: relative;
}
.spacer{
    flex-grow: 1;
}
h1{
    color:white;
    text-align:center;
}
</style>
