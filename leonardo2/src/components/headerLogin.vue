<template>
    <v-app-bar app color="#2A3F54">
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
    </v-app-bar>
</template>

<script>
export default {
    data() {
        return{
            help:''
        }
    },
    props:{
        ajuda:{
            type: String
        }
    },
    methods:{
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
        if(this.ajuda == 'login'){
            this.help = 'Esta é a ajuda do login'
        }
        else if(this.ajuda == 'registo'){
            this.help = 'Esta é a ajuda da página de registo'
        }
    }
}
</script>

<style scoped>
.v-toolbar__content, .v-toolbar__extension{
    position: relative;
}
</style>
