<template>
  <v-app-bar app color="#2A3F54" height="100" clipped-left>
    <v-list nav dense dark color="#2A3F54">
      <v-list-item two-line class="px-0">
        <v-list-item-avatar
          min-width="55px"
          tile
          class="ava"
          @click="about = true"
        >
          <v-img src="" />
          <!-- Imagem que ao ser clicada abre um dialog descritivo do projeto -->
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title><h2>Título do Projeto</h2></v-list-item-title>
          <v-list-item-subtitle>Título do Sistema</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <div class="spacer"></div>
    <!-- Ativar a mudança de língua-->
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <!-- @click="Função para por língua como Português,
        utilizando o i18n ou outra biblioteca" -->
        <v-btn text small class="white--text change-font" v-on="on">PT</v-btn>
      </template>
      <span>Português</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <!-- @click="Função para por língua como Espanhol,
        utilizando o i18n ou outra biblioteca" -->
        <v-btn text small class="white--text change-font" v-on="on">ES</v-btn>
      </template>
      <span>Espanhol</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <!-- @click="Função para por língua como Inglês, utilizando o i18n ou outra biblioteca"  -->
        <v-btn text small class="white--text change-font" v-on="on">UK</v-btn>
      </template>
      <span>Inglês</span>
    </v-tooltip>
    <!-- Menú do cabeçalho-->
    <v-menu>
      <template v-slot:activator="{ on: menu }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on: tooltip }">
            <v-btn fab v-on="{ ...tooltip, ...menu }">
              <v-avatar>
                <!-- :src="Foto, possivelmente do utilizador" -->
                <v-img />
              </v-avatar>
            </v-btn>
          </template>
          <span>
            <!-- {{ $t('header.opPerfil') }} -->
          </span>
        </v-tooltip>
      </template>
      <v-list>
        <!-- :to="Se se quiser meter página específica a ser acedida no menu do cabeçalho" -->
        <v-list-item link>
          <v-list-item-title>Página para mudar</v-list-item-title>
        </v-list-item>
        <!-- Se se quiser fazer logout -->
        <v-list-item @click="logout()" text>
          <!-- <v-list-item-title>{{ $t('head.exit') }}</v-list-item-title> -->
        </v-list-item>
      </v-list>
    </v-menu>
    <v-list-item-group>
      <v-list-item disabled dark>
        <v-list-item-content>
          <v-list-item-title> Nome do utilizador </v-list-item-title>
          <v-list-item-subtitle>
            Tipo de utilizador (administrador, utilizador normal,etc.)
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-app-bar>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      parametro: ''
    }
  },
  methods: {
    logout() {
      // Função de logout
      axios.get()
    }
  }
}
</script>

<style scoped>
/* css do cabeçalho */
.v-toolbar__content,
.v-toolbar__extension {
  position: relative;
}
.spacer {
  flex-grow: 1;
}
h1 {
  color: white;
  text-align: center;
}
</style>
