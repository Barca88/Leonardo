<template>
  <div class="text-center">
    <v-dialog
      persistent
      v-model="this.alertPopup.dialog"
      width="500"
    >
      <v-card>
        <v-card-title class="headline headColor">
            {{ this.alertPopup.header }}
        </v-card-title>

        <div>
        <v-img id="icon" max-height="50" max-width="50" src="@/assets/info.png" v-if="this.alertPopup.type == 'info'"></v-img>
        <v-img id="icon" height="50" max-width="50" src="@/assets/del.png" v-if="this.alertPopup.type == 'del'"></v-img>
        <v-img id="icon" max-height="50" max-width="50" src="@/assets/warn.png" v-if="this.alertPopup.type == 'warn'"></v-img>
        <v-card-text v-html="this.alertPopup.message"></v-card-text>
        </div>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="#FF1744" @click="confirmed()" v-if="this.alertPopup.confirmB"> <v-icon>mdi-check</v-icon> </v-btn>
          <v-btn color="#00E676" @click="close()" > <v-icon>mdi-door-open</v-icon> </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  export default {
    props: ['alertPopup'],
    data () {
      return {
          confirmPromise: undefined
      }
    },
    methods:{
        close (){
            this.alertPopup.dialog = false
            if(this.alertPopup.type === "confirm") this.confirmPromise(false)
        },
        confirmed (){
            this.alertPopup.dialog = false
             if(this.alertPopup.type === "confirm") this.confirmPromise(true)
        },
        async trigger (opts = {}){
            this.alertPopup = opts
            await new Promise(r => setTimeout(r, 10))
            this.alertPopup.dialog = true

            return new Promise(confirmed => {
                this.confirmPromise = confirmed
            })
        },
        async display (opts = {}){
            this.alertPopup = opts
            await new Promise(r => setTimeout(r, 10))
            this.alertPopup.dialog = true
        }
    }
  }
</script>

<style scoped>
#icon{
    margin: 20px;
    float: left;
}
.headColor {
    background-color: #01579B;
}
</style>
