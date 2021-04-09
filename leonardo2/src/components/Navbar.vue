<template>
  <nav>
    <v-toolbar flat color='#2A3F54'>
      <v-spacer></v-spacer> 
      <!--
      <div class="flag" @click="setLocale('pt')">
        <img class="mx-2 mt-2" :src="require('../assets/portugal.png')" height="30"/> 
      </div>
      <div class="flag" @click="setLocale('en')">
        <img class="mt-2" :src="require('../assets/uk.png')" height="30"/>
      </div>
      <div class="flag" @click="setLocale('es')">
        <img class="mx-2 mt-2" :src="require('../assets/spain.png')" height="19"/> 
      </div> 
      -->
      <v-tooltip bottom> 
        <template v-slot:activator="{ on }">
        <v-btn text small class="white--text change-font" v-bind:class="{active: activeBtn === 'btn1' }" @click="setLocale('pt'); activeBtn = 'btn1'" v-on="on">PT</v-btn>
        </template>
        <span>{{ $t('nav.LinguaPT') }}</span>
      </v-tooltip>

      <v-tooltip bottom> 
        <template v-slot:activator="{ on }">
        <v-btn text small class="white--text change-font" v-bind:class="{active: activeBtn === 'btn2' }" @click="setLocale('es'); activeBtn = 'btn2'" v-on="on">ES</v-btn>
        </template>
        <span>{{ $t('nav.LinguaES') }}</span>
      </v-tooltip>
      
      <v-tooltip bottom> 
        <template v-slot:activator="{ on }">
        <v-btn text small class="white--text change-font"  v-bind:class="{active: activeBtn === 'btn3' }" @click="setLocale('en'); activeBtn = 'btn3'" v-on="on">UK</v-btn>
        </template>
        <span>{{ $t('nav.LinguaEN') }}</span>
      </v-tooltip>

    </v-toolbar>
  </nav>
</template>

<script>
//import Popup from './Popup'; 
//import DropdownMenu from './DropdownMenu';

export default {
  components: {},
  data() {
    return {
      closeOnContentClick: true, 
      filterBtnTTip: false,  
      activeBtn: 'btn1'
    };
  }, 
  methods:{ 
    setLocale(locale){ 
      this.$i18n.locale = locale
      this.$router.push({
        params: { lang: locale }
      })
    }
  } 
};
</script>

<style>
.flag:hover {
  cursor: pointer;
} 
.active{
  background-color:#29b89b;
}
</style>

<style lang="stylus" scoped>
.change-font {
    font-family: "Arial";
}
</style>