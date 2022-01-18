<template>
  <div class="text-center">
    
    <v-dialog @keydown.esc="dialog = false" v-model="dialog" scrollable width="500">
      <template v-slot:activator="{ on }">
        <v-btn depressed text class="grey--text change-font text-none" v-on="on">
          <span class="change-font">{{ $t('nav.buttonAjuda') }}</span>
        </v-btn>
      </template>
      <v-card>
        <v-card-title class="headline change-font">{{ $t('nav.buttonAjuda') }}</v-card-title>
        
        <v-divider
        class="mx-4"
        horizontal
       ></v-divider>

      
      
      <v-card-text class="change-font" style="white-space: pre-line"
          >{{ $t('nav.textoInstrucoes') }}</v-card-text
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