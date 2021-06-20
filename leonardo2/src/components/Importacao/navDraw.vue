<template>
    <v-card>
        <v-navigation-drawer app clipped v-if="drawerOn" permanent :expand-on-hover="expandOnHover" :mini-variant="miniVariant" color='#2A3F54' class="navBar" >

          <v-list nav dense dark >
            <v-divider light></v-divider>
            <!-- List group se for uma secção da barra de navegação lateral que se divida em subsecções-->
<!--             <v-list-group class="white--text" prepend-icon="icon mdi" :value="false" no-action > -->
<!--               <template v-slot:activator> -->
<!--                 <v-list-item-title class="white--text">Nome Secção</v-list-item-title> -->
<!--               </template> -->
<!--                   <v-list-item link to="Link Subsecção 1"> -->
<!--                     <v-list-item-title class="white--text">Nome Subsecção 1</v-list-item-title> -->
<!--                   </v-list-item> -->
<!--                   <v-list-item link to="Link Subsecção 2"> -->
<!--                     <v-list-item-title class="white--text">Nome Subsecção 2</v-list-item-title> -->
<!--                   </v-list-item> -->
<!--                   ... -->
<!--             </v-list-group> -->
            <!-- List item se não se dividir em subsecções-->
            <v-list-item link to="/import">
                <v-list-item-icon>
                  <v-icon>mdi-paperclip</v-icon>
                </v-list-item-icon>
                <v-list-item-title class="white--text"> Importação de questões</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/errors">
                <v-list-item-icon>
                  <v-icon>mdi-alert</v-icon>
                </v-list-item-icon>
                <v-list-item-title class="white--text"> Verificação de erros</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/">
                <v-list-item-icon>
                  <v-icon>mdi-magnify</v-icon>
                </v-list-item-icon>
                <v-list-item-title class="white--text"> Verificação de questões</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/dashboard">
                <v-list-item-icon>
                 <!-- mdi-chart-box-outline -->
                  <v-icon>mdi-chart-box-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title class="white--text"> Dashboard de importação</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/settings">
                <v-list-item-icon>
                  <v-icon>mdi-cog</v-icon>
                </v-list-item-icon>
                <v-list-item-title class="white--text"> Definições</v-list-item-title>
            </v-list-item>
          </v-list>
          <template v-slot:append>
            <div class="pa-2">
              <!-- Botão de fixação da barra de navegação lateral-->
              <v-btn dark depressed min-width="60px" @click="fixNav()" >
                <v-icon>mdi-axis-arrow-lock</v-icon>
              </v-btn>
              <!-- Botão de logout-->
              <v-btn dark depressed min-width="60px" @click="logout();">
                <v-icon>mdi-power</v-icon>
              </v-btn>
            </div>
          </template>
        </v-navigation-drawer>
    </v-card>
</template>

<script>
/*import axios from 'axios'*/
export default {
    data() {
        return{
            miniVariant: true,
            expandOnHover: true,
            drawerOn: true
        }
    },
    methods:{
      logout: function(){
        //função de logout
      },
      //função de fixação da barra de navegação lateral
      fixNav: function(){
        this.expandOnHover=!this.expandOnHover
        this.miniVariant=!this.miniVariant
        this.drawerOn=false
        this.$nextTick(() =>
          this.drawerOn = true
        )
      }
    }
};
</script>

<style scoped>
/* css da barra de navegação lateral */
header{
    background:#2A3F54;
    padding: 10px;
}

h1{
    color:white;
    text-align:center;
}
.navBar{
  text-align: left;
}
h3{
    color:white;
}
.ava{
  margin-top: 50px;
}
</style>
