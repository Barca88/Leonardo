<template>
  <v-navigation-drawer
    app
    clipped
    v-if="drawerOn"
    permanent
    :expand-on-hover="expandOnHover"
    :mini-variant="miniVariant"
    color="#2A3F54"
    class="navBar"
  >
    <v-list nav dense dark>
      <v-divider light />

      <!-- Testes -->
      <v-list-group
        class="white--text"
        prepend-icon="mdi-file-document-outline"
        :value="false"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-title class="white--text"> Testes </v-list-item-title>
        </template>

        <v-list-item link to="/tests/management">
          <v-list-item-icon>
            <v-icon v-text="'mdi-file-multiple-outline'" />
          </v-list-item-icon>
          <v-list-item-title class="white--text">
            Gestao de Testes
          </v-list-item-title>
        </v-list-item>

        <v-list-item link to="/tests/evaluation">
          <v-list-item-icon>
            <v-icon v-text="'mdi-file-check-outline'" />
          </v-list-item-icon>
          <v-list-item-title class="white--text"> Avaliacao </v-list-item-title>
        </v-list-item>
      </v-list-group>

      <!-- Estatisticas -->
      <v-list-group
        class="white--text"
        prepend-icon="mdi-chart-box-outline"
        :value="false"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-title class="white--text">
            Estatisticas
          </v-list-item-title>
        </template>

        <v-list-item link to="/tests/results">
          <v-list-item-icon>
            <v-icon v-text="'mdi-chart-bell-curve'" />
          </v-list-item-icon>
          <v-list-item-title class="white--text">
            Resultados
          </v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
    <template v-slot:append>
      <div class="pa-2">
        <v-btn dark depressed min-width="60px" @click="fixNav()">
          <v-icon v-text="'mdi-axis-arrow-lock'" />
        </v-btn>
        <v-btn dark depressed min-width="60px" @click="logout()">
          <v-icon v-text="'mdi-power'" />
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
// import axios from 'axios';
export default {
  data() {
    return {
      miniVariant: true,
      expandOnHover: true,
      drawerOn: true,
    };
  },
  methods: {
    logout() {
      // funcao de logout
    },
    // funcao de fixacao da barra de navegacao lateral
    fixNav() {
      this.expandOnHover = !this.expandOnHover;
      this.miniVariant = !this.miniVariant;
      this.drawerOn = false;
      this.$nextTick(() => {
        this.drawerOn = true;
      });
    },
  },
};
</script>

<style scoped>
/* css da barra de navegacao lateral */
header {
  background: #2a3f54;
  padding: 10px;
}

h1 {
  color: white;
  text-align: center;
}
.navBar {
  text-align: left;
}
h3 {
  color: white;
}
.ava {
  margin-top: 50px;
}
</style>
