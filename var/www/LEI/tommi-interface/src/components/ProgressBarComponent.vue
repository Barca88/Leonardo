<template>
  <v-container fill-height>
    <v-row align="center" justify="center">
      <p>Aguarde o processamento dos Fólios</p>
      <v-col cols="12">
        <div style="min-height: 500px;">
          <v-progress-linear indeterminate color="blue darken-2" ></v-progress-linear>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from 'axios'
const lhost = 'https://tommi2.di.uminho.pt/api'
export default {
  mounted: async function () {
    try {
      var response = await axios.get(lhost + '/process', {headers: { 'Authorization': `Bearer: ${this.$store.state.jwt}`}})
      if(response.data.message){
        this.$router.push('/localidades')
      }
    } catch (e) {
      return e
    }
  }
}
</script>
