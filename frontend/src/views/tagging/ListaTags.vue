<template>
  <div>
    <Header></Header>
    <div v-if="this.$store.state.user.tipo === 'Admin'">
      <NavDraw></NavDraw>
    </div>
    <div v-else>
      <NavDrawLeitor></NavDrawLeitor>
    </div>
    <div>
      <ListaTagsComponent />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ListaTagsComponent from "@/components/tagging/ListaTagsComponent.vue";
import NavDraw from '@/components/navDraw.vue'
import NavDrawLeitor from '@/components/navDrawLeitor.vue'
import Header from '@/components/header.vue'

export default {
  name: "Home",
  components: {
    Header,
    ListaTagsComponent,
    NavDraw,
    NavDrawLeitor
  },
};
</script>
