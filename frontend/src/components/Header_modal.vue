<template>
  <v-app-bar color="#172d44" dark>
    <div class="d-flex align-center">
      <v-img alt="Vuetify Logo" class="shrink mr-2" contain :src="require('../assets/raccoon.png')" transition="scale-transition" width="80" style="margin-left:20px;"/>
      <h4 width="40">Leonardo - </h4> <h5>Plataforma de Avaliação e de Estudo</h5>
    </div>
  </v-app-bar>
</template>

<script>
  export default {
    name: 'Header_modal',
  }
</script>