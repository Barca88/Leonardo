<template>
  <v-app>
    <v-content>      
      <router-view></router-view>
      <!--<appFooter></appFooter>-->
    </v-content>
  </v-app>
</template>

<script>
//import Footer from './components/Footer.vue'
export default {
  name: 'App',

  /*components: {
    'appFooter':Footer
  },*/

  data: () => ({
    //
  }),
};
</script>

<style scoped>

</style>
