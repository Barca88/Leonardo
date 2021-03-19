<template>
    <div id="folios">
      <appHeader ></appHeader>
      <div v-if="this.$store.state.user.tipo === 'Admin'" >
        <navDraw></navDraw>
      </div>
      <div v-else>
        <navDrawLeitor></navDrawLeitor>
      </div>
      <div>
          <placeListComponent></placeListComponent>
      </div>
    </div>
</template>
<script>
import axios from 'axios'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
import placeListComponent from '../components/PlaceListComponent.vue'
export default {
    components:{
        'appHeader': Header,
        'navDraw':NavDraw,
        'navDrawLeitor':navDrawLeitor,
        'placeListComponent': placeListComponent
    },
    created() {
        axios.get(`https://tommi2.di.uminho.pt/api/folios/folios?nome=admin`,{headers:{
          Authorization:`Bearer: ${this.$store.state.jwt}`
        }})
        .then(response => {
            // JSON responses are automatically parsed.
            //console.log(response.data)
            this.folios = response.data.folios
        }).catch(e => {
            //console.log(e)
            this.errors.push(e)
        })
    }
}
</script>
<style scoped>
    /* .tommitable .v-data-table .table{ */
   .v-data-table /deep/ th{
        background-color:#4b779e;
    }
    .v-data-table /deep/ tr{
        color: #73879C;
        font-size: 13px;
    }
    .v-data-table /deep/ tr:nth-child(even){
        background-color: lightgray;
    }
    #folios *{
            box-sizing: border-box;
    }
    #folios{
            margin: 20px auto;
            max-width: 1100px;
            margin-bottom: 80px;
    }
    label {
        color: white;
        padding: 8px;
        font-family: Arial, sans-serif;
        font-weight: bold;
        font-size: 15px;
    }
    b{
        font-size: 14px;
    }
</style>
