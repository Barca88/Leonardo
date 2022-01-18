<template>
  <div>
    <GmapMap
      :center="{lat:41.5518, lng:-8.4229}"
      :zoom="11"
      :map-type-id= viewType
      style="width: 970px; height: 900px"
    >
      <GmapMarker
        v-for="(place,index) in places"
        :key="index"
        :label="place.nome"
        :position="google && new google.maps.LatLng(place.latitude,place.longitude)"
        :clickable="true"
        :draggable="false"
        @click="showDialog(place.nome)"
      />
       <v-dialog
      v-model="showOptions"
      max-width="190"
    >
      <v-card>
        <v-card-title class="headline">{{ place }}</v-card-title>
        <v-card-text>
         Fólios
        </v-card-text>
        <v-card-text>
         Propriétarios
        </v-card-text>
        <v-card-text>
         Terras
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="showOptions = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </GmapMap>
  </div>
</template>
<script>
import { gmapApi } from 'vue2-google-maps'
export default {
  props: ['viewType', 'places'],
  data () {
    return {
      showOptions: false,
      place: ''
    }
  },
  methods: {
    showDialog (local) {
      this.place = local
      this.showOptions = true
    }
  },
  computed: {
    google: gmapApi
  }
}
</script>
