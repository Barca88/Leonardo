<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <v-row>
          <v-col cols="3">
            <v-btn @click="typeTerrain"> Terrain  </v-btn>
          </v-col>
          <v-col cols="3">
            <v-btn @click="typeSatellite"> Satelite </v-btn>
          </v-col>
          <v-col cols="3">
            <v-btn @click="typeRoadMap"> RoadMap </v-btn>
          </v-col>
          <v-col cols="3">
            <v-btn @click="typeHybrid"> Hybrid </v-btn>
          </v-col>
        </v-row>
        <hr>
        <MapComponent :viewType="viewType" :places="places"></MapComponent>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
// import axios from 'axios'
import MapComponent from '@/components/MapComponent.vue'
// const lhost = 'http://localhost:5000'
export default {
  data: function () {
    return {
      componentSelected: 'Terrain',
      viewType: 'terrain',
      places: []
    }
  },
  components: {
    "MapComponent":MapComponent
  },
  methods: {
    typeTerrain () {
      this.componentSelected = 'Terrain'
      this.viewType = 'terrain'
    },
    typeSatellite () {
      this.componentSelected = 'Satellite'
      this.viewType = 'satellite'
    },
    typeRoadMap () {
      this.componentSelected = 'RoadMap'
      this.viewType = 'roadmap'
    },
    typeHybrid () {
      this.componentSelected = 'Hybrid'
      this.viewType = 'hybrid'
    }
  },
  created: function () {
    var obj = {
      nome: this.$route.query.nome,
      latitude: this.$route.query.latitude,
      longitude: this.$route.query.longitude
    }
    this.places.push(obj)
  }
}
</script>
