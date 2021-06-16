<template>
  <div>
    <NavBar />
    <NavDraw />
    <v-main>
      <router-view />
    </v-main>
    <Footer />
  </div>
</template>

<script>
import NavBar from "@/components/header.vue";
import NavDraw from "@/components/navDraw.vue";
import Footer from "@/components/footer2.vue";

export default {
  name: "App",
  components: { Footer, NavBar, NavDraw },
};
</script>
