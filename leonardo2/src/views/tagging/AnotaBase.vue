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
      <AnotaBaseComponent />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import AnotaBaseComponent from "@/components/tagging/AnotaBaseComponent.vue";
import NavDraw from '@/components/navDraw.vue'
import NavDrawLeitor from '@/components/navDrawLeitor.vue'
import Header from '@/components/header.vue'

export default {
  name: "Atualiza",
  components: {
    Header,
    AnotaBaseComponent,
    NavDraw,
    NavDrawLeitor
  },
};
</script>
