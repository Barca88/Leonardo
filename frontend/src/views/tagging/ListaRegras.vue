<template>
  <div>
    <Header></Header>
    <div v-if="this.$store.state.user.type === 'Admin'">
      <NavDraw></NavDraw>
    </div>
    <div v-else>
      <NavDrawLeitor></NavDrawLeitor>
    </div>
    <div>
      <ListaRegrasComponent />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ListaRegrasComponent from "@/components/tagging/ListaRegrasComponent.vue";
import NavDraw from '@/components/navDraw.vue'
import NavDrawLeitor from '@/components/navDrawLeitor.vue'
import Header from '@/components/header.vue'

export default {
  name: "Home",
  components: {
    Header,
    ListaRegrasComponent,
    NavDraw,
    NavDrawLeitor
  },
};
</script>
