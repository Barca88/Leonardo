<template>
  <div class="text-center">
    <v-dialog @keydown.esc="dialog = false" v-model="dialog" scrollable width="500">
      <template v-slot:activator="{ on }">
        <v-btn depressed text class="grey--text change-font text-none" v-on="on">
          <span class="change-font">{{ $t('nav.sabermais') }}</span>
        </v-btn>
      </template>
      <v-card>
        <v-toolbar color="#2A3F54" dark>
            <h2>{{ $t('nav.sabermais') }}</h2>
        </v-toolbar>

        <v-divider
        class="mx-4"
        horizontal
        ></v-divider>

        <v-card-text class="change-font mt-6" style="white-space: pre-line"
            >{{ $t('nav.textoSaberMais') }}</v-card-text
        >
        <v-card-actions>
            <v-spacer></v-spacer>
            
            <v-tooltip bottom> 
            <template v-slot:activator="{ on }">
                <v-btn depressed color="white" @click="dialog=false" v-on="on">
                    <v-icon large>mdi-exit-to-app</v-icon>
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