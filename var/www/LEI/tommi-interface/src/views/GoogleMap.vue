<template>
    <div>
    <appHeader ></appHeader>
      <div v-if="this.$store.state.user.tipo === 'Admin'" >
        <navDraw></navDraw>
      </div>
      <div v-else>
        <navDrawLeitor></navDrawLeitor>
      </div>
      <div>
          <GoogleMapComponent />
      </div>
  </div>
</template>
<script>
import GoogleMapComponent from '@/components/GoogleMapComponent.vue'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
// @ is an alias to /src
export default {
  name: 'GoogleMap',
  components: {
    'appHeader': Header,
    'navDraw':NavDraw,
    'navDrawLeitor':navDrawLeitor,
    'GoogleMapComponent': GoogleMapComponent
    
  }
}
</script>
