<template>
  <v-footer color="white">
    
    <v-row 
    justify="center" 
    > 

    <PopupCreditos /> 
    <PopupSaberMais /> 
    <PopupTermos /> 
    <PopupPrivacidade /> 
    <Popup />

    <v-col 
    cols="12" 
    > 
      <div class="text-center"> 
          <small class="grey--text change-font text-none">©Tommi, 2020</small> 
      </div>
    </v-col>
    </v-row>
  
  
  </v-footer>
</template>

<script>
import PopupTermos from './PopupTermos'; 
import PopupCreditos from './PopupCreditos'; 
import PopupSaberMais from './PopupSaberMais'; 
import PopupPrivacidade from './PopupPrivacidade';  
import Popup from './Popup'
//import DropdownMenu from './DropdownMenu';

export default {
  components: {PopupTermos,PopupCreditos,PopupSaberMais,PopupPrivacidade, Popup},
  data() {
    return {};
  }, 
}
</script>

<style lang="stylus" scoped>
.change-font {
    font-family: "Arial";
}
</style>