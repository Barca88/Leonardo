<template>
  <div class="text-center">
    
    <v-dialog @keydown.esc="dialog = false" v-model="dialog" scrollable width="500">
      <template v-slot:activator="{ on }"> 
        <!-- Já está igual ao login tb a imagem -->
        <v-img class="center" max-height="150px" max-width="150px" src="../assets/logo_original.png" v-on="on"></v-img> 
      </template>
      <v-card>
        <v-card-title class="headline change-font">{{ $t('nav.SistemaTommiHeader') }}</v-card-title>

         <v-divider
        class="mx-4"
        horizontal
       ></v-divider>

        <v-card-text class="change-font" style="white-space: pre-line"
          >{{ $t('nav.SistemaTommiExpli') }}</v-card-text
        >
        <v-card-actions>
          <v-spacer></v-spacer>
                                    
          <v-tooltip bottom> 
            <template v-slot:activator="{ on }">
                <v-btn depressed color="white" @click="dialog=false" v-on="on">
                  <v-icon large>mdi-door-open</v-icon>
                </v-btn>
              </template>
              <span>{{ $t('nav.Sair') }}</span>
            </v-tooltip>

        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog: false
    };
  }
};
</script>

<style lang="stylus" scoped>
.change-font {
    font-family: "Arial";
}
</style> 

<style scoped>
 .center {
    margin-top: 1cm;
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 50%;
  }
</style>