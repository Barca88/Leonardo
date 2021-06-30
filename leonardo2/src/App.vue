<template>
  <v-app>
    <appHeader v-if="$route.path!='/login'" :ajuda='ajuda' @toggleDrower="toggle=!toggle"></appHeader>
    <navDraw v-if="$route.path!='/login'" :toggle="toggle"></navDraw> 
    <v-main>      
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import NavDraw from './components/navDraw.vue'
import Header from './components/header.vue'
//import Footer from './components/Footer.vue'
export default {
  name: 'App',
  data() { 
    return {
      toggle: true
  }},
  components:{
      'appHeader': Header,
      'navDraw':NavDraw
  }
};
</script>

<style scoped>

</style>
