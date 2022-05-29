<template>
    <v-card style="border-radius:0px;">
        <v-img :src="image" max-width="100%"></v-img>
    </v-card>
</template>

<script>
  export default {
    name: 'Image_dialog',

    props: ['filename'],

    computed: {
        image(){ 
            return require("../assets/" + this.filename); 
        }
    }
  }
</script>